#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'erika.ochiai'

from collections import defaultdict
import math
import sys

def create_features(title):
    features = defaultdict(float)
    for word in title.split(' '):
        features['UNI:'+word] += 1
    return features

def sign_value(value):
    if value >= 0:
        ret = 1
    else:
        ret = -1
    return ret

def update_weights(w, phi, y, c=0.0001):
    for name, value in w.iteritems():
        if abs(value) < c:
            w[name] = 0
        else:
            w[name] -= sign_value(value) * c
    for name, value in phi.iteritems():
        w[name] += value * y
    return w

def calculate_margin(w, phi, y):
    sum = 0.
    for name, value in phi.iteritems():
        if name in w:
            sum += value * w[name]
    return sum * y


def training_svm(input_file, output_file):
    margin = 0.
    w = defaultdict(float)
    with open(input_file, 'r') as fr:
        for line in fr:
            answer, title = line.rstrip().split('\t')
            phi = create_features(title)
            val = calculate_margin(w, phi, float(answer))
            if val <= margin:
                w = update_weights(w, phi, float(answer))
    with open(output_file, 'w') as fw:
        for name, value in sorted(w.iteritems(), key=lambda x:x[0]):
            weight = '{0}\t{1:.6f}\n'.format(name, value)
            fw.write(weight)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Please input training data file and output file as trained data.')
        sys.exit(1)
    training_svm(sys.argv[1], sys.argv[2])

