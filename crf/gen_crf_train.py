#!/usr/bin/env python
# encoding: utf-8

import sys
import re
import time
import marisa_trie

def build_trie(words, charset = 'utf-8'):
    '''
    build trie with unicode words
    '''
    uni_words = [w.decode(charset, 'ignore') for w in words]
    trie = marisa_trie.Trie(uni_words)
    return trie

def match_trie(trie, text, charset = 'utf-8'):
    '''
    match with all prefixes
    '''
    uni_str = text.decode(charset, 'ignore')
    i = 0
    L = len(uni_str)
    results = []
    for i in range(L):
        hits = trie.prefixes(uni_str[i:])
        if hits:
            results.extend(hits)
    a = [x.encode(charset) for x in set(results)]
    return a

def match_trie2(trie, text, charset = 'utf-8'):
    '''
    match with the longest prefix
    '''
    uni_str = text.decode(charset, 'ignore')
    i = 0
    L = len(uni_str)
    results = []
    while i < L:
        hits = trie.prefixes(uni_str[i:])
        if hits:
            max_len = 0
            max_word = ''
            for w in hits:
                n = len(w)
                if n > max_len:
                    max_len = n
                    max_word = w
            results.append(max_word)
            i += len(max_word)
        else:
            i += 1
    a = [x.encode(charset) for x in set(results)]
    return a


def gen_crf_train_data(text, words, charset ='utf-8'):
    '''
    gen crf train data
    four tags: B M E O
    '''
    uni_str = text.decode(charset, 'ignore')
    uwords = [w.decode(charset) for w in words]
    i = 0
    L = len(uni_str)
    results = []
    while i < L:
        hit = 0
        for uword in uwords:
            if uni_str.startswith(uword, i):
                n = len(uword)
                if n > 2:
                    results.append("%s\tB" % uword[0])
                    for ix in range(1,n-1):
                        results.append("%s\tM" % uword[ix])
                    results.append("%s\tE" % uword[-1])
                elif n == 2:
                    results.append("%s\tB" % uword[0])
                    results.append("%s\tE" % uword[1])
                elif n == 1:
                    results.append("%s\tO" % uword[0])
                i += n
                hit = 1
                break
        if hit == 0:
            results.append("%s\tO" % uni_str[i])
            i += 1
    res = '\n'.join(results).encode(charset)
    return res

def do_taggging(conf_file, infile, text_field, out_file):
    '''
    do tagging
    '''
    # build trie
    tag_words = set()
    for line in file(conf_file):
        s = line.strip('\n').split('\t')
        word = s[0]
        if word.find('`') != -1:
            continue
        word = word.replace(" ","`") #note whitespace
        tag_words.add(word)
    trie = build_trie(tag_words)

    # match
    fout = open(out_file, 'w')
    for line in file(infile):
        line = line.rstrip('\n')
        s = line.split('\t')
        text = s[text_field].replace(" ", "`") #note whitespace
        words = match_trie2(trie, text)
        if words:
            res = gen_crf_train_data(text, words)
            fout.write("%s\n\n" % res)
            print "%s\t%s" % (line, ';'.join(words))
    fout.close()

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "usage: %s <conf_file> <infile> <text_field> <out_file>" % __file__
        sys.exit(-1)

    text_field = int(sys.argv[3])
    do_taggging(sys.argv[1], sys.argv[2], text_field, sys.argv[4])
