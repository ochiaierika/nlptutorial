#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'erika.ochiai'
import sys
from collections import defaultdict

def save_trained_hmm(output_file, emit, transit, context):
    with open(output_file, 'w') as f:
        for k, v in sorted(transit.iteritems(), key=lambda x:x[0]):
            tag, _ = k.split(' ')
            f.write('T %s %6f\n' % (k, float(v)/context[tag]))

        for k, v in sorted(emit.iteritems(), key=lambda x:x[0]):
            tag, _ = k.split(' ')
            f.write('E %s %6f\n' % (k, float(v)/context[tag]))


def train_hmm(training_data):
    emit, transit, context = defaultdict(int), defaultdict(int), defaultdict(int)
    with open(training_data, 'r') as f:
        for line in f:
            prev = '<s>'
            context[prev] += 1
            for tagged_word in line.rstrip().split(' '):
                word, tag = tagged_word.split('_')
                context[tag] += 1
                transit[prev+' '+tag] += 1
                emit[tag+' '+word] += 1
                prev = tag
            transit[prev+' </s>'] += 1
    return emit, transit, context

if __name__ == '__main__':
    if len(sys.argv) is not 3:
        print('Please input training file and output file which is saved with trained data.')
        sys.exit(1)

    emit, transit, context = train_hmm(sys.argv[1])
    save_trained_hmm(sys.argv[2], emit, transit, context)

