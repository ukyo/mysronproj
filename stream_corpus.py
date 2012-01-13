#!/usr/bin/python

# onlinewikipedia.py: Demonstrates the use of online VB for LDA to
# analyze a bunch of random Wikipedia articles.
#
# Copyright (C) 2010  Matthew D. Hoffman
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import cPickle, string, numpy, getopt, sys, random, time, re, pprint

import streamlda
from util import print_topics
import json
import MeCabParser

def main():
    """
    Applies streamLDA to test data, currently either 20 newsgroups or
    wikipedia. The wikipedia option downloads and analyzes a bunch of random
    Wikipedia articles using online VB for LDA. This is nice for breadth of
    examples, but is not precisely repeatable since the articles are random. 20
    newsgroups provides data on which a repeatable run can be performed.
    """

    # The number of documents to analyze each iteration
    batchsize = 64
    # The number of topics
    K = 50

    tweets = open(sys.argv[1], 'r')
    runs = int(sys.argv[2])        
    
    parser = MeCabParser.Parser()
    
    def parse(d):
        return parser.parse(d, to_unicode=True)
    
    # Initialize the algorithm with alpha=1/K, eta=1/K, tau_0=1024, kappa=0.7
    slda = streamlda.StreamLDA(K, 1./K, 1./K, 1., 0.7, parse=parse)

    test_set = []
    for i in range(batchsize):
        t = json.loads(tweets.readline())['text']
        test_set.append(t)
    
    for iteration in xrange(0, runs):
        print '-----------------------------------'
        print '         Iteration %d              ' % iteration
        print '-----------------------------------'
        
        docset = []
        for i in range(batchsize):
            tweet = json.loads(tweets.readline())['text']
            docset.append(tweet)
        # Give them to online LDA
        (gamma, bound) = slda.update_lambda(docset)
        # Compute an estimate of held-out perplexity
        wordids = slda.recentbatch['wordids']
        wordcts = slda.recentbatch['wordcts']
        #(wordids, wordcts) = slda.parse_new_docs(docset)

        if iteration % 10 == 0:
          gamma_test, new_lambda = slda.do_e_step(test_set)
          new_lambda = None
          lhood = slda.batch_bound(gamma_test)

          print_topics(slda._lambda, 10)
          print "Held-out likelihood", lhood

if __name__ == '__main__':
    main()
