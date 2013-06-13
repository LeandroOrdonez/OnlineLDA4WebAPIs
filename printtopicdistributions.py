#!/usr/bin/python

# printtopics.py: Prints the per-document topic distributions (based on
# the 'printtopics.py' script by Matthew D. Hoffman)
#
# Copyright (C) 2013 Leandro Ordonez
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
    Displays the per-document topic distribution fit by onlineldavb.py. The first column gives the
    (expected) most prominent topics in the document, the second column
    gives their (expected) relative prominence.
    """
    #vocab = str.split(file(sys.argv[1]).read())
    gamma = numpy.loadtxt(sys.argv[1])
    if(len(sys.argv) > 2):
        topics_per_document = int(sys.argv[2])
    else:
        topics_per_document = 10

    topics_file = open('outcome/per-document-topics.txt', 'w')
    for d in range(0, len(gamma)):
        thetad = list(gamma[d, :])
        thetad = thetad / sum(thetad)
        temp = zip(thetad, range(1, len(thetad)+1))
        temp = sorted(temp, key = lambda x: x[0], reverse=True)
        print 'Operation (Id) %d:' % (d+1)
	topics_file.write('Operation (Id) %d:' % (d))
        # feel free to change the "53" here to whatever fits your screen nicely.
        for i in range(0, topics_per_document):
            print '\t Topic %s  \t---\t  %.4f' % (temp[i][1], temp[i][0])
	    topics_file.write('\t Topic %s  \t---\t  %.4f' % (temp[i][1], temp[i][0]))
        print
	topics_file.write('\n')
    topics_file.close()

if __name__ == '__main__':
    main()
