#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NLP Tutorial
Section.2: n-gram model
Exercise.1: Training bi-gram
"""

from __future__ import division
import sys
from collections import defaultdict


def train_2gram(input_file, trained_model):
    counts, context_counts = defaultdict(int), defaultdict(int)
    with open(input_file, 'r') as f:
        for line in f:
            line = line.rstrip().split(' ')
            line.insert(0, '<s>')
            line.append('</s>')
            for i in range(1, len(line)):
                counts[' '.join(line[i-1:i+1])] += 1
                counts[line[i]] += 1
                context_counts[line[i-1]] += 1
                context_counts[''] += 1
    # calculate probability
    with open(trained_model, 'w') as ft:
        for n_gram, count in sorted(counts.iteritems(), key=lambda x:x[0]):
            n_gram_words = n_gram.split(' ')
            n_gram_context = n_gram_words[:-1]
            prob = count / context_counts[' '.join(n_gram_context)]
            ft.write('%s\t%6f\n' % (n_gram, prob))


if __name__ == '__main__':
    if len(sys.argv) is not 3:
        print('Please set file name which you want to train & output into.')
    train_2gram(sys.argv[1], sys.argv[2])
