#!/usr/bin/python

# jsonify.py: Generates a JSON file from the per-document topic 
# distribution fitted by onlineldavb.py
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

import numpy as np

"""
Generates a JSON file from the per-document topic distribution fitted by 
onlineldavb.py
"""

def run():
    pdc = np.loadtxt('../../outcome/per-document-topics.csv', dtype={'names': \
('Operation ID', 'Operation Name', 'Topic', 'Topic Probability', 'Terms'),\
'formats': ('i4', 'S100', 'i4', 'f4', 'S400')}, delimiter=',', skiprows=1)
    pcd = sorted(pdc, key = lambda x: x[2])
# print pdt[0:5]
# print ptd[0:5]

    doc_categories = dict()
    for doc in pdc:
        if int(doc[3]*1000) > 150:
            key = (doc[0], doc[1])
#    print key
            if (not key in doc_categories):
                doc_categories[key] = [('Category-'+`doc[2]`, int(doc[3]*1000))]
            else:
                doc_categories[key].append(('Category-'+`doc[2]`, int(doc[3]*1000)))
#print doc_topics

    category_docs = dict()
    for category in pcd:
        if int(category[3]*1000) > 150:
            key = 'Category-'+`category[2]`
            if (not key in category_docs):
                category_docs[key] = [(category[0], category[1])]
            else:
                category_docs[key].append((category[0], category[1]))
#print topic_docs

    json_output = '' + \
"""{
    "name": "categories",
    "children": [
    %s
    ]
   }""" % jsonify_categories(category_docs, doc_categories)
    
    print json_output
    #np.savetxt('../../outcome/per-document-topics.json', json_output)
    pdc_json_file = open('../../outcome/per-document-topics.json', 'w')
    pdc_json_file.write(json_output)
    pdc_json_file.close()

def jsonify_categories(category_docs, doc_categories):
    #print 'entro a jsonify_categories'
    result = ''
    for category in category_docs:
        result += \
'{\n    "name": "' + category + \
'", \n    "children": [\n %s\n]\n},' % jsonify_documents(category_docs[category], doc_categories)
    #print result[:-1]
    return result[:-1]

def jsonify_documents(docs, doc_categories):
    #print 'entro a jsonify_documents'
    result = ''
    for doc in docs:
        result += \
'{\n    "name": "' + doc[1] + \
'", \n    "children": [\n %s\n]\n},' % jsonify_cat_per_doc(doc_categories[doc])
    #print result[:-1]
    return result[:-1]

def jsonify_cat_per_doc(categories):
    #print 'entro a jsonify_cat_per_doc'
    result = ''
    for category in categories:
        result += \
'{"name": "' + category[0] + '", "size": ' + `category[1]` + '},'
    #print result[:-1]    
    return result[:-1]

if __name__ == '__main__':
    run()
