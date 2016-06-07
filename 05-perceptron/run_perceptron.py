#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'erika.ochiai'

import sys


def judgement(score):
    if score >= 0.:
        return 1
    return -1

def load_trained_perceptron(trained_data_file):
    weighted_dict = dict()
    with open(trained_data_file, 'r') as f:
        for line in f:
            line = line.rstrip().split('\t')
            weighted_dict[line[0]] = float(line[1])
    return weighted_dict

def run_perceptron(trained_file, test_file):
    phi = load_trained_perceptron(trained_file)
    with open(test_file) as f:
        for line in f:
            score = 0.
            for word in line.rstrip().split(' '):
                key = 'UNI:' + word
                if key in phi:
                    score += phi[key]
            value = judgement(score)
            print('{}\t{}'.format(value, line.rstrip()))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Please input trained perceptron file and test file.')
        sys.exit(1)
    run_perceptron(sys.argv[1], sys.argv[2])
