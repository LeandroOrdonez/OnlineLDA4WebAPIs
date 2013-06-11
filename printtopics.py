#!/usr/bin/python

# printtopics.py: Prints the words that are most prominent in a set of
# topics.
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

import sys, os, re, random, math, urllib2, time, cPickle
import numpy

import onlineldavb

def main():
    """
    Displays topics fit by onlineldavb.py. The first column gives the
    (expected) most prominent words in the topics, the second column
    gives their (expected) relative prominence.
    """
    vocab = str.split(file(sys.argv[1]).read())
    testlambda = numpy.loadtxt(sys.argv[2])
    if(len(sys.argv) > 3):
        words_per_topic = int(sys.argv[3])
    else:
        words_per_topic = 5

    topics_file = open('outcome/topics.txt', 'w')
    for k in range(0, len(testlambda)):
        lambdak = list(testlambda[k, :])
        lambdak = lambdak / sum(lambdak)
        temp = zip(lambdak, range(0, len(lambdak)))
        temp = sorted(temp, key = lambda x: x[0], reverse=True)
        print 'topic %d:' % (k)
	topics_file.write('topic %d: \n' % (k))
        # feel free to change the "53" here to whatever fits your screen nicely.
        for i in range(0, words_per_topic):
            print '%20s  \t---\t  %.4f' % (vocab[temp[i][1]], temp[i][0])
	    topics_file.write('%20s  \t---\t  %.4f \n' % (vocab[temp[i][1]], temp[i][0]))
        print
	topics_file.write('\n')
    topics_file.close()

if __name__ == '__main__':
    main()
