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


def check_hmm(trained_file, test_file):
    trans, emission, possible_tags = load_hmm_model(trained_file)
    with open(test_file, 'r') as f:
        for line in f:
            best_score, best_edge = defaultdict(int), defaultdict(int)
            best_score['0 <s>'] = 0.
            best_edge['0 <s>'] = None
            words = line.rstrip().split(' ')
            l = len(words)

            for i in range(0, l):
                # prev
                for prev in possible_tags.keys():
                    for current in possible_tags.keys():
                        score = 0.
                        if '{} {}'.format(i, prev) in best_score and '{} {}'.format(prev, current) in trans:

                            trans_prob_log = math.log(trans['{} {}'.format(prev, current)], 2)

                            emission_prob = (1.-LAMB) / N
                            if emission['{} {}'.format(current, words[i])] != 0.0:
                                emission_prob += LAMB * emission['{} {}'.format(current, words[i])]
                            emission_prob_log = math.log(emission_prob, 2)

                            score = best_score['{} {}'.format(i, prev)] - trans_prob_log - emission_prob_log
                        if '{} {}'.format(i+1, current) not in best_score or best_score['{} {}'.format(i+1, current)] < score:
                            best_score['{} {}'.format(i+1, current)] = score
                            if i == 0:
                                best_edge['{} {}'.format(i+1, current)] = '{} {}'.format(i, '<s>')
                            else:
                                best_edge['{} {}'.format(i+1, current)] = '{} {}'.format(i, prev)

            for prev in possible_tags.keys():
                if '{} {}'.format(l, prev) in best_score and '{} {}'.format(prev, '</s>') in trans:
                    trans_prob_log = 0.0
                    if trans['{} {}'.format(prev, '</s>')] != 0.0:
                        trans_prob_log = math.log(trans['{} {}'.format(prev, '</s>')], 2)
                    score = best_score['{} {}'.format(l, prev)] - trans_prob_log
                    if '{} {}'.format(l+1, '</s>') not in best_score \
                            or best_score['{} {}'.format(l+1, '</s>')] < score:
                        best_score['{} {}'.format(l+1, '</s>')] = score
                        best_edge['{} {}'.format(l+1, '</s>')] = '{} {}'.format(l, prev)

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
