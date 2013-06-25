#!/usr/bin/python

# printtopicdistributions.py: Prints the per-document topic distributions (based on
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
import rdf_sesame.model_instantiation as rdfmi
import rdf_sesame.sesamehandler as sesame

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
	if(topics_per_document > len(gamma[0])):
            print 'Warning: the maximum number of topics allowed is', len(gamma[0])
            topics_per_document = len(gamma[0])
    else:
        topics_per_document = 10

    topics_file = open('outcome/per-document-topics.txt', 'w')
    # Creating a Sesame repository handler (with default values).
    repo = sesame.SesameHandler()
    for d in range(0, len(gamma)):
        thetad = list(gamma[d, :])
        thetad = thetad / sum(thetad)
        temp = zip(thetad, range(0, len(thetad)))
        temp = sorted(temp, key = lambda x: x[0], reverse=True)
        print 'Operation (Id) %d:' % (d+1)
	topics_file.write('Operation (Id) %d: \n' % (d+1))
        # Storing the documents (operations) and the categories they belong to as RDF statements.
        membership_relations = list()
        rdf_data = ''
        for i in range(0, topics_per_document):
            print '\t Topic %s  \t---\t  %.4f' % (temp[i][1], temp[i][0])
	    topics_file.write('\t Topic %s  \t---\t  %.4f \n' % (temp[i][1], temp[i][0]))
            membership_relation = rdfmi.new_membership_relation(`(d+1)` + ';' + `temp[i][1]`, temp[i][0], `temp[i][1]`)
            membership_relations.append(`(d+1)` + ';' + `temp[i][1]`)
            rdf_data = rdf_data + membership_relation
        operation = rdfmi.new_operation(`(d+1)`, membership_relations)
        rdf_data = rdf_data + operation
        repo.post_statement(rdf_data)
        print
	topics_file.write('\n')
    topics_file.close()

if __name__ == '__main__':
    main()
