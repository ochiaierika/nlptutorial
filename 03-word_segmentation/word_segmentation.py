#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'erika.ochiai'
import sys
import math
from collections import defaultdict

VOCAB_NUMBER = 10 ** 6
UNKNOWN_PROB = 0.05


def load_trained_model(train_file):
    trained_model = defaultdict(float)
    with open(train_file, 'r') as f:
        for line in f:
            word, prob = line.rstrip().split('\t')
            trained_model[unicode(word, 'utf-8')] = float(prob)
    return trained_model


def forward_facing_step(trained_model, line):
    best_edge = dict()
    best_score = dict()
    best_edge[0] = None
    best_score[0] = 0.
    for word_end in range(1, len(line) + 1):
        best_score[word_end] = 10 ** 10
        for word_begin in range(0, word_end):
            word = line[word_begin:word_end]
            if word in trained_model or len(word) is 1:
                prob = UNKNOWN_PROB / VOCAB_NUMBER
                if word in trained_model:
                    prob += (1. - UNKNOWN_PROB) * trained_model[word]
                my_score = best_score[word_begin] - math.log(prob, 2)
                if my_score < best_score[word_end]:
                    best_score[word_end] = my_score
                    best_edge[word_end] = (word_begin, word_end)
    return best_edge


def backward_facing_step(best_edge, line):
    words = list()
    next_edge = best_edge[len(best_edge) - 1]
    while next_edge:
        word = line[next_edge[0]:next_edge[1]]
        word = word.encode('utf-8')
        words.append(word)
        next_edge = best_edge[next_edge[0]]
    words.reverse()
    return words


def word_segmentation(trained_file, test_file):
    """
    To segment word with trained data (uni-gram)
    :param trained_file: file name which has trained data with uni-gram
    :param test_file: file name of test data
    """
    trained_model = load_trained_model(trained_file)

    with open(test_file, 'r') as f:
        for line in f:
            line = unicode(line.rstrip(), 'utf-8')
            best_edge = forward_facing_step(trained_model, line)
            words = backward_facing_step(best_edge, line)
            print ' '.join(words)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Please input trained file and test file.')
        sys.exit(1)
    word_segmentation(sys.argv[1], sys.argv[2])
