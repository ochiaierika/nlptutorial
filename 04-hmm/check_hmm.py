#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'erika.ochiai'
from collections import defaultdict
import math
import sys
N = 10**6
LAMB = 0.95

def load_hmm_model(input):
    trans, emission, possible_tags = defaultdict(float), defaultdict(float), defaultdict(float)
    with open(input, 'r') as f:
        for line in f:
            type, context, word, prob = line.rstrip().split(' ')
            possible_tags[context] = 1
            if type is 'T':
                trans[context+' '+word] = float(prob)
            else:
                emission[context+' '+word] = float(prob)
    return trans, emission, possible_tags


def calc_prob(key, dic, smoothing=False):
    N = 10**6
    LAMB = 0.95
    prob = 0.
    if smoothing is True:
        if key in dic:
            prob = dic[key]
    else:
        prob = (1.-LAMB) / N
        if key in dic:
            prob += LAMB * dic[key]
    return prob

def check_hmm(trained_file, test_file):
    trans, emission, possible_tags = load_hmm_model(trained_file)
    with open(test_file, 'r') as f:
        for line in f:
            best_score, best_edge = dict(), dict()
            best_score['0 <s>'] = 0.
            best_edge['0 <s>'] = None
            words = line.rstrip().split(' ')
            l = len(words)
            # forward
            #   first
            for current in possible_tags.keys():
                best_key = '1 ' + current
                trans_key = '<s> ' + current
                emiss_key = '<s> ' + words[0]
                score = -math.log(calc_prob(trans_key, trans), 2) - math.log(calc_prob(emiss_key, emission), 2)
                best_score[best_key] = score
                best_edge[best_key] = '0 <s>'

            #   middle
            for i in range(1, l):
                for prev in possible_tags.keys():
                    for current in possible_tags.keys():
                        prev_key = '{} {}'.format(i, prev)
                        trans_key = '{} {}'.format(prev, current)
                        emiss_key = '{} {}'.format(current, words[i])

                        if prev_key in best_score:
                            score = best_score[prev_key] - math.log(calc_prob(trans_key, trans), 2) - math.log(calc_prob(emiss_key, emission), 2)

                        current_key = '{} {}'.format(i+1, current)
                        if current_key not in best_score or best_score[current_key] > score:
                            best_score[current_key] = score
                            best_edge[current_key] = prev_key

            #   end
            for prev in possible_tags:
                prev_key = '{} {}'.format(l, prev)
                trans_key = '{} {}'.format(prev, '</s>')

                if prev_key in best_score:
                    score = best_score[prev_key] - math.log(calc_prob(trans_key, trans), 2)

                current_key = '{} {}'.format(l+1, '</s>')
                if current_key not in best_score or best_score[current_key] > score:
                    best_score[current_key] = score
                    best_edge[current_key] = prev_key


            # backward
            tags = []
            next_edge = best_edge['{} {}'.format(l+1, '</s>')]
            while next_edge != "0 <s>":
                position, tag = next_edge.split(' ')
                tags.append(tag)
                next_edge = best_edge[next_edge]
            tags.reverse()
            print ' '.join(tags)


if __name__ == '__main__':
    if len(sys.argv) is not 3:
        print('Please input your file name. - Trained data with HMM and test data file')
        sys.exit(1)
    check_hmm(sys.argv[1], sys.argv[2])
