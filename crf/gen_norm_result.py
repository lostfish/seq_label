#!/usr/bin/env python
# encoding: utf-8

import sys

def gen_crf_test_data(infile, out_file, charset ='utf-8'):
    '''
    gen crf test data
    '''
    fout = open(out_file, 'w')
    a = []
    b = []
    words = []
    with open(infile) as f:
        for line in f:
            if line == '\n': #sentence end
                text = ''.join(a).replace('`', ' ')
                if words:
                    info = '%s\t%s\n' % (text, ';'.join(words))
                    fout.write(info)
                a = []
                b = []
                words = []
                continue

            s = line.rstrip('\n').split('\t')
            ch = s[0]
            tag = s[2]
            a.append(ch)
            if tag == 'B' or tag == 'M':
                b.append(ch)
            elif tag == 'E':
                b.append(ch)
                words.append(''.join(b))
                b = []
            else:
                b = []
    fout.close()

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print "usage: %s <infile> <out_file>" % __file__
        sys.exit(-1)

    gen_crf_test_data(sys.argv[1], sys.argv[2])
