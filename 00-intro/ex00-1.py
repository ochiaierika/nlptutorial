# -*- coding: utf8 -*-
__author__ = 'erika.ochiai'
import os

def main():
    input_file = os.path.expanduser('~/research/practice/nlptutorial/test/00-input.txt')
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
        print ('{} {}'.format(char, count))


if __name__=='__main__':
    main()
