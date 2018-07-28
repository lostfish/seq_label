#!/usr/bin/env python
# encoding: utf-8

import sys
import re
import time

def do_eval(gold_file, pred_file):
    '''Evaluate crf predicted result

    File format: text <tab> entity1;entity2;...
    '''
    map1 = {}
    map2 = {}
    for line in file(gold_file):
        s = line.rstrip('\n').split('\t')
        words = set(s[1].split(';'))
        map1[s[0]] = words
    for line in file(pred_file):
        s = line.rstrip('\n').split('\t')
        words = set(s[1].split(';'))
        map2[s[0]] = words

    N = 0 # real total amount
    n = 0 # recalled amount
    for k,v in  map1.iteritems():
        N += len(v)
        if k in map2:
            v2 = map2[k]
            x = len(v & v2)
            n += x
            if x != len(v):
                print "diff:\t%s\t%s\t%s" % (k, ';'.join(list(v)), ';'.join(list(v2)))

    M = 0 # predicted total amount
    for k,v in  map2.iteritems():
        M += len(v)
        if k not in map1:
            print "new:\t%s\t%s" % (k, ';'.join(list(v)))

    precision = float(n)/M
    recall = float(n)/N
    print "precision:\t%d\t%d\t%.3f" % (n, M, precision)
    print "recall:\t%d\t%d\t%.3f" % (n, N, recall)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "usage: %s <gold_file> <pred_file>" % __file__
        print "file format: text <tab> entity1;entity2;..."
        sys.exit(-1)
    do_eval(sys.argv[1], sys.argv[2])
