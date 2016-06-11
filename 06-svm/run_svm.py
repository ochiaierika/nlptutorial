#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'erika.ochiai'

from collections import defaultdict
import math
import sys

def load_svm_data(input_file):
    w = defaultdict(float)
    with open(input_file, 'r') as f :
        for line in f:
            name, value = line.rstrip().split('\t')
            w[name] = float(value)
    return w

def create_features(title):
    phi = defaultdict(float)
    for word in title.split(' '):
        phi['UNI:'+word] += 1.
    return phi



def run_svm(trained_file, input_file, output_file):
    w = load_svm_data(trained_file)
    with open(input_file, 'r') as fr, open(output_file, 'w') as fw:
        for line in fr:
            phi = create_features(line.rstrip())
            w_phi = 0.
            for name, value in phi.iteritems():
                w_phi += w[name] * value
            if w_phi >= 0:
                answer = 1
            else:
                answer = -1
            string = '{}\t{}'.format(answer, line)
            fw.write(string)



if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Please input trained data, test data and output file.')
        sys.exit(1)
    run_svm(sys.argv[1], sys.argv[2], sys.argv[3])
