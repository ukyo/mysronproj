#encoding: utf8

import re
import unicodedata
from HTMLParser import HTMLParser

MAX_LENGTH = 20000

parser = HTMLParser()

default_normalize_methods = [
    'twitter_http',
    'twitter_reply',
    'decode_entities',
    'strip_html',
    'strip_nl',
    'strip_single_nl',
    'unify_whitespaces',
    'wavetilde2long',
    'fullminus2long',
    'dashes2long',
    'drawing_lines2long',
    'unify_long_repeats',
    'nfkc', 'lc', 'renzoku'
]

def gen_sub(pattern, repl):
    p = re.compile(pattern)
    return lambda s: p.sub(repl, s)

br2nl = gen_sub('<br(\s*(\"[^\"]*\"|[^>])*)?>[\n\r]?', '\n')
p2nl = gen_sub('<\/?p(\s+(\"[^\"]*\"|[^>])*)?>[\n\r]?', '\n')
strip_tag = gen_sub('<(\"[^\"]*\"|[^>])*>', '')
strip_entity = gen_sub('&#?[a-zA-Z0-9]+;?', '')
strip_tag = gen_sub('[\n\r]', '')
strip_single_tag = gen_sub('([\n\r]?)([\n\r]+)', '\n')
wavetilde2long = gen_sub(u'[\u301c\uff5e]', u'\u30fc')
fullminus2long = gen_sub(u'\u2212', u'\u30fc')
dashes2long = gen_sub(u'[\u2012\u2013\u2014\u2015\u2053\u301c\u3030]', u'\u30fc')
drawing_lines2long = gen_sub(u'[\u2500\u2501\u254C\u254D\u2574\u2576\u2578\u257A]', u'\u30fc')
unify_long_repeats = gen_sub(u'\u30fc{2,}', u'\u30fc')
unify_whitespace = gen_sub('\s+', ' ')
renzoku = gen_sub(r'(.)\1{2,}', r'\1\1')
twitter_http = gen_sub("https?://[A-Za-z0-9\'~+\-=_.,/%\?!;:@#\*&\(\)]+",'')
twitter_reply = gen_sub('(@|#)[a-zA-Z0-9]+', '')

class TextNormalizer(object):

    def __init__(self, *normalize_methods):
        self.normalize_methods = normalize_methods if len(normalize_methods) else default_normalize_methods
    
    def normalize(self, s):
        for method in self.normalize_methods:
            s = getattr(self, method, lambda x: x)(s)
        return s
    
    def decode_entities(self, s):
        return parser.unescape(s)
    
    def strip_html(self, s):
        if len(s) > MAX_LENGTH:
            s = s[:MAX_LENGTH]
        s = br2nl(s)
        s = p2nl(s)
        s = strip_tag(s)
        s = strip_entity(s)
        return s
    
    def strip_nl(self, s):
        return strip_tag(s)
    
    def strip_single_nl(self, s):
        return strip_single_tag(s)
    
    def unify_whitespaces(self, s):
        return unify_whitespace(s)
    
    def wave2tilde(self, s):
        return wavetilde2long(s)
    
    def wavetilde2long(self, s):
        return wavetilde2long(s)
    
    def fullminus2long(self, s):
        return fullminus2long(s)
    
    def dashes2long(self, s):
        return dashes2long(s)
    
    def drawing_lines2long(self, s):
        return drawing_lines2long(s)
    
    def unify_long_repeats(self, s):
        return unify_long_repeats(s)
    
    def nfkc(self, s):
        return unicodedata.normalize('NFKC', s)
    
    def nfkd(self, s):
        return unicodedata.normalize('NFKD', s)
    
    def nfc(self, s):
        return unicodedata.normalize('NFC', s)
    
    def nfd(self, s):
        return unicodedata.normalize('NFD', s)
    
    def lc(self, s):
        return s.lower()
    
    def renzoku(self, s):
        return renzoku(s)
    
    def twitter_http(self, s):
        return twitter_http(s)
    
    def twitter_reply(self, s):
        return twitter_reply(s)