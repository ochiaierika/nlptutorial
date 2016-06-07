#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'erika.ochiai'

from collections import defaultdict
import sys

def train_perceptron(input_file, trained_file):
    phi = defaultdict(float)
    with open(input_file, 'r') as f:
        for line in f:
            answer, text = line.rstrip().split('\t')
            for word in text.split(' '):
                phi['UNI:'+word] += float(answer)

    with open(trained_file, 'w') as fw:
        for word, weight in sorted(phi.iteritems(), key=lambda x:x[0]):
            string = '{0}\t{1:.6f}\n'.format(word, weight)
            fw.write(string)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Please input labeled file and output file.')
        sys.exit(1)
    train_perceptron(sys.argv[1], sys.argv[2])
