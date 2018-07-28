#!/usr/bin/env python
# encoding: utf-8

import sys

def gen_crf_test_data(infile, text_field, charset ='utf-8'):
    '''
    gen crf test data
    '''
    with open(infile) as f:
        for line in f:
            s = line.rstrip('\n').split('\t')
            text = s[text_field].replace(" ", "`") #note whitespace
            a = []
            for ch in text.decode(charset, 'ignore'):
                a.append("%s\tO" % ch)
            res = '\n'.join(a).encode(charset)
            print "%s\n" % res

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print "usage: %s <infile> <text_field>" % __file__
        sys.exit(-1)

    gen_crf_test_data(sys.argv[1], int(sys.argv[2]))
