# -*- coding: utf-8 -*-

from datetime import datetime
import nltk
import random

train_set = []
test_set = []
word_features = []

def get_word_features(messages, top_features, only_ngrams):
    all_words = []
    for (words, sender) in messages:
        if not only_ngrams: all_words.extend(words)
        bigrams = nltk.bigrams(words)
        trigrams = nltk.trigrams(words)
        all_words.extend([' '.join(b) for b in bigrams])
        all_words.extend([' '.join(t) for t in trigrams])

    freq = nltk.FreqDist(all_words)
    top_features = len(freq.keys()) if top_features == 0 else top_features
    most_common = [f[0] for f in freq.most_common(top_features)]
    print '# filtered words incl. ngrams: ' + str(len(all_words))
    print '# filtered unique words incl. ngrams: ' + str(len(freq.keys()))
    print '# feature words: ' + str(len(most_common))
    print '# feature words of size 1: ' + str(len([w for w in most_common if len(w.split()) == 1]))
    print '# feature words of size 2: ' + str(len([w for w in most_common if len(w.split()) == 2]))
    print '# feature words of size 3: ' + str(len([w for w in most_common if len(w.split()) == 3]))
    print 'Top 20 words: ' + ', '.join(most_common[:20]) + '\n----'

    return most_common

def get_message_features(message, word_features, only_ngrams):
    bigrams = nltk.bigrams(message)
    trigrams = nltk.trigrams(message)

    message_words = set() if only_ngrams else set(message)
    message_words = message_words.union([' '.join(b) for b in bigrams])
    message_words = message_words.union([' '.join(t) for t in trigrams]) 

    features = {}
    for word in word_features:
        features['c(%s)' % word] = (word in message_words)
    
    return features

def compute_train_test(messages, top_features=0, only_ngrams=False):
    global train_set, test_set, word_features
    word_features = get_word_features(messages, top_features, only_ngrams)
    featuresets = [(get_message_features(m, word_features, only_ngrams), l) for (m, l) in messages]
    random.shuffle(featuresets)
    train_set, test_set = featuresets[:-5000], featuresets[-5000:]

# Takes message vectors as generated by messages_to_vectors
def train_classifier():
    global train_set
    start = datetime.now()
    c = nltk.NaiveBayesClassifier.train(train_set)
    print 'Training time: ' + str((datetime.now() - start).total_seconds()) + ' s'
    return c