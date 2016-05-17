# -*- coding: utf8 -*-
from __future__ import division
import sys


def main(input_file):
    count_uni = dict()
    total = 0
    with open(input_file, 'r') as f:
        for line in f:
            line = line.rstrip().split(' ')
            line.append('</s>')
            for word in line:
                if word in count_uni:
                    count_uni[word] += 1
                else:
                    count_uni[word] = 1
                total += 1

    for word, count in sorted(count_uni.iteritems(), key=lambda x:x[0]):
        print('%s\t%f' % (word, count/total))


if __name__=='__main__':
    if len(sys.argv) < 2:
        print('Please set the training file. ')
    input_file = sys.argv[1]
    main(input_file)