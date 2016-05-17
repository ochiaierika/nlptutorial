#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from collections import defaultdict
import sys
import math

__author__ = 'erika.ochiai'

V = 1000000


def calculate_2gram_entropy(model_file, test_file, param1, param2):
    h, w = 0, 0
    # load trained model data
    trained_model = defaultdict(float)
    with open(model_file, 'r') as f:
        for line in f:
            words, prob = line.rstrip().split('\t')
            trained_model[words] = float(prob)
    with open(test_file, 'r') as f:
        for line in f:
            line = line.rstrip().split(' ')
            line.insert(0, '<s>')
            line.append('</s>')

            for i in range(1, len(line)):
                p_uni = param1 * trained_model[line[i]] + (1. - param1) / V
                p_bi = param2 * trained_model[' '.join(line[i-1:i+1])] + (1. - param2) * p_uni
                h -= math.log(p_bi, 2)
                w += 1
    entropy = h / w
    print('Entropy is %f' % entropy)


if __name__ == '__main__':
    if len(sys.argv) is not 5:
        print('Please input model file and test file.')
        sys.exit(1)
    calculate_2gram_entropy(sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))

