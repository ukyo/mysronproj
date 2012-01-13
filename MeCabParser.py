#!/usr/bin/python

import os
from NormalizeText import TextNormalizer
import MeCab

HOME = os.environ["HOME"]
default_option = "-d %s/mecab-ipadic-2.7.0-20070801 -u %s/mecab-dic-overdrive/misc/dic/wikipedia.dic" % (HOME, HOME)

class Parser(object):
    def __init__(self, encoding="utf8", mecab_option=default_option):
        self.encoding = encoding
        self.mecab_option = mecab_option
        self.tagger = MeCab.Tagger(self.mecab_option)
        self.normalizer = TextNormalizer()
    
    def parse(self, s, to_unicode=False):
        if type(s) == str:
            s = s.decode(self.encoding)
        s = self.normalizer.normalize(s).encode(self.encoding)
        node = self.tagger.parseToNode(s)
        ret = []
        while node:
            surface = node.surface
            if surface != "":
                if to_unicode:
                    surface = surface.decode(self.encoding)
                ret.append(surface)
            node = node.next
        return ret

if __name__ == '__main__':
    parser = Parser()
    while 1:
        for x in parser.parse(raw_input("input:" ), to_unicode=True):
            print x