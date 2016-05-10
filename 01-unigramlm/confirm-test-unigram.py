# -*- coding: utf8 -*-
from __future__ import division
import sys
import math
from collections import defaultdict

VOCAB_NUMBER = 10**6
UNKNOWN_PROB = 0.05


def load_trained_model(train_file):
    trained_model = dict()
    with open(train_file, 'r') as f:
        for line in f:
            word, prob = line.rstrip().split('\t')
            trained_model[word] = (1. - UNKNOWN_PROB) * float(prob) + UNKNOWN_PROB * 1./ VOCAB_NUMBER
    # add unknown_word prob
    trained_model[None] = UNKNOWN_PROB * 1./ VOCAB_NUMBER
    return trained_model

def load_trained_data(train_file):
    trained_model = defaultdict(float)
    with open(train_file, 'r') as f:
        for line in f:
            word, prob = line.rstrip().split('\t')
            trained_model[word] = float(prob)
    return trained_model

def main(train_file, test_file):
    trained_prob = load_trained_model(train_file)
    total_count, covered_word_count = 0, 0
    entropy = 0.
    with open(test_file, 'r') as f:
        for line in f:
            line = line.rstrip().split(' ')
            line.append('</s>')
            for word in line:
                if word in trained_prob:
                    entropy -= math.log(trained_prob[word],2)
                    covered_word_count += 1
                else:
                    entropy -= math.log(trained_prob[None],2)
                total_count += 1
            # EOS
            #entropy -= math.log(trained_prob['</s>'], 2)
            #covered_word_count += 1
            #total_count += 1

    print ('entropy = %f' % (entropy / total_count))
    print ('coverage = %f' % (covered_word_count / total_count))


def test_unigram(train_file, test_file):

    total_words, unknown_words, h = 0, 0, 0
    trained_dic = load_trained_data(train_file)
    with open(test_file, 'r') as f:
        for line in f:
            line = line.rstrip().split(' ')
            line.append('</s>')
            for word in line:
                total_words += 1
                p = UNKNOWN_PROB / VOCAB_NUMBER
                if word in trained_dic:
                    p += (1. - UNKNOWN_PROB) * trained_dic[word]
                else:
                    unknown_words += 1
                h -= math.log(p, 2)
    print('Entropy: {}'.format(h/total_words))
    print('Coverage: {}'.format((total_words-unknown_words)/total_words))

if __name__=='__main__':
    if len(sys.argv) < 3:
        print("Please set uni-gram files.\npython [trained file] [test file]")
    train_file = sys.argv[1]
    test_file = sys.argv[2]
    main(train_file, test_file)
    #test_unigram(train_file, test_file)
