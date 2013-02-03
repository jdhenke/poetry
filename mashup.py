#!/usr/bin/python

'''

MARKOV MODEL MASHUPS

Creates 'lyrical mashups' using Markov Models.
Can use characters or words as state. (You should add more mediums!)

Example files used:
    mashup.py       # this script
    sonnets.txt     # all of shakespeare's sonnets
    rhcp.txt        # all of red hot chili peppers lyrics
    gaga.txt        # all of lady gaga's lyrics

Input:
    ./mashup.py sonnets.txt              # randomly generate text similar to
                                         # shakespeare's sonnets
    
    ./mashup.py sonnets.txt rhcp.txt     # mashup shakespeare and the RHCP

    ./mashup.py *.txt                    # mashup all three

    ./mashup.py mimic.py                 # inception

Output:
    prints to stdout a variety of mashups
    modify main() to fit your needs!

Copyright (c) 2013 Joseph Henke

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.

'''

# BUGS
#   1) Could reach the "end", where has not experienced a following state
#   2) doesn't evenly weight all files specified. should be option.
#   3) perhaps not bug, but assumes random seed is fine. 
#      maybe have option to provide seed?

from abc import *
import re, sys, random

def main():
    '''parses command line. creates model. prints mashup.'''
    paths = sys.argv[1:]
    assert len(paths) > 0, 'No paths specified.'
    max_order = 3
    # quick and dirty way to display results from different handlers
    for handler, length in ((CharacterHandler(), 60), (WordHandler(), 10)):
        print 'Using %s' % (handler, )
        for order in xrange(1, max_order + 1):
            mm = MarkovModel(order, handler, paths)
            text = mm.mashup(length)
            print '\t Order %i => %s' % (order, text, )

class DataHandler(object):
    '''Base class for extracting different data from files'''
    __metaclass__ = ABCMeta
    @abstractmethod
    def get_data(path):
        pass
    @abstractmethod
    def data_to_str(path, data):
        pass
    @abstractmethod
    def __str__(self):
        pass

class CharacterHandler(DataHandler):
    '''use characters except new lines'''
    def get_data(self, path):
        return tuple([x for x in open(path).read() if x not in ('\n', '\r', )])
    def data_to_str(self, data):
        return ''.join(data)
    def __str__(self):
        return 'Letters'

class WordHandler(DataHandler): 
    '''use your words! (delimited by whitespace)'''
    def get_data(self, path):
        return tuple([x for x in re.split('\s+', open(path).read()) if len(x) > 0])
    def data_to_str(self, data):
        return ' '.join(data)
    def __str__(self):
        return 'Words'

class MarkovModel(object):
    
    def __init__(self, order, handler, paths):
        self.order = order
        self.handler = handler
        self.distro = self.get_distribution(paths)

    def get_distribution(self, paths):
        '''
        returns dictionary:
            keys = state
            values = list of (datum, cdf)
                example:
                    counts[state] = {'A':3, 'C':6, 'B':3}
                    distro[state] = [('A', 0), ('C', .25), ('B', .75)] 

        - guarantees cdfs will be in increasing order
        - no guarantees on order of data elements
        - cdfs will NOT sum to 1; in fact will never
            - this convention is useful in choose_next()
        '''

        counts = {}
        for path in paths:
            path_counts = self.get_transitions(counts, path)
        distro = {}
        for state, next_letters in counts.iteritems():
            total = 1.0 * sum(next_letters.values())
            distro[state] = []
            cdf = 0.0
            for letter, count in next_letters.iteritems():
                distro[state].append((letter, cdf))
                cdf += count / total
        return distro

    def get_transitions(self, counts, path):
        '''modifies counts to include data from path'''
        data = self.handler.get_data(path)
        for i in xrange(len(data) - self.order):
            state = tuple(data[i:i+self.order])
            counts.setdefault(state, {})
            datum = data[i+self.order]
            counts[state].setdefault(datum, 0)
            counts[state][datum] += 1
            
    def mashup(self, n):
        '''returns string mashup of length n based on this model'''
        state = random.choice(self.distro.keys())
        data = []
        for i in xrange(n):
            datum = self.choose_next(self.distro[state])
            data.append(datum)
            state = state[1:] + (datum, )
        return self.handler.data_to_str(data)

    def choose_next(self, options):
        '''chooses random datum based on probabilities'''
        r = random.random()
        last = None
        for datum, prob in options:
            if r < prob:
                return last
            else:
                last = datum
        return last

if __name__ == '__main__':
    main()

