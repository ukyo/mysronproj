#!/usr/bin/python
#encoding: utf8

import sys
from NormalizeText import TextNormalizer

if __name__ == '__main__':
    #print sys.argv
    if len(sys.argv) < 2:
        normalizer = TextNormalizer()
    else:
        normalizer = TextNormalizer(*sys.argv[1:])
    #print normalizer.normalize_methods
    while 1:
        s = raw_input()
        print normalizer.normalize(s.decode('utf8'))