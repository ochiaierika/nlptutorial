# -*- coding: utf8 -*-
__author__ = 'erika.ochiai'
import sys


def main(input_file):
    char_dic = dict()
    with open(input_file, 'r') as f:
        for line in f:
            chars = line.rstrip().split(' ')
            for char in chars:
                if char in char_dic:
                    char_dic[char] += 1
                else:
                    char_dic[char] = 1

    for char, count in sorted(char_dic.iteritems(), key=lambda x: x[0]):
        print ('{}\t{}'.format(char, count))


if __name__=='__main__':
    if len(sys.argv) < 2:
        print('Please set the training ')
    input_file = sys.argv[1]
    main(input_file)