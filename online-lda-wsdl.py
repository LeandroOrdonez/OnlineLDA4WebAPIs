import cPickle, string, numpy, getopt, sys, random, time, re, pprint, os

import onlineldavb
#import wikirandom

def get_file_content(n, batchsize, path):
    content = list()
    ids = list()
    set_size = len(os.listdir(path))
    lower = (batchsize*n - (batchsize - 1)) % set_size
    if (batchsize*n) % set_size != 0:
        upper = (batchsize*n) % set_size + 1
    else:
	upper = set_size + 1
    _range = range(lower, upper)
    #print _range
    for i in _range:
	file_name = path + str(i) + '.txt'
        all = file(file_name).read()
        content.append(all)
	#print all
        ids.append(i)
    return (content, ids)


def main():
    """
    Retrieves the content of a set of text files whose content is obtained
    from SOAP API descriptors.
    """
    path = sys.argv[1]
    docs = os.listdir(path)

    # The number of documents to analyze each iteration
    rest = 1
    #batchsize = len(docs)
    batchsize = 4
    print len(docs)
    while rest != 0:
        rest = len(docs) % batchsize
        if (rest != 0):
            batchsize = batchsize + 1
        
    # The total number of documents (is supposed to be a huge/infinite number in an online setting)
    D = 3.3e6
    #D = len(docs)
    # The number of topics
    K = 40

    # How many documents to look at
    #print batchsize
    #print sys.argv[0]
    if (len(sys.argv) == 2):
        #print 'Got into IF...'
        documentstoanalyze = int(len(docs)/batchsize)
    elif (len(sys.argv) == 3):
        documentstoanalyze = int(sys.argv[2])
    elif (len(sys.argv) == 4):
        documentstoanalyze = int(sys.argv[2])
        K = int(sys.argv[3])

    
    print documentstoanalyze
    # Our vocabulary
    vocab = file('./dictnostops.txt').readlines()
    W = len(vocab)

    # Initialize the algorithm with alpha=1/K, eta=1/K, tau_0=1024, kappa=0.7
    olda = onlineldavb.OnlineLDA(vocab, K, D, 1./K, 1./K, 1024., 0.7)
    #olda = onlineldavb.OnlineLDA(vocab, K, D, 0.01, 0.01, 1024., 0.7)
    # Run until we've seen D documents. (Feel free to interrupt *much*
    # sooner than this.)
    for iteration in range(1, documentstoanalyze+1):
        # Download some articles
        (docset, operation_id) = \
            get_file_content(iteration, batchsize, path)
        # Give them to online LDA
        (gamma, bound) = olda.update_lambda(docset)
        # Compute an estimate of held-out perplexity
        (wordids, wordcts) = onlineldavb.parse_doc_list(docset, olda._vocab)
        perwordbound = bound * len(docset) / (D * sum(map(sum, wordcts)))
        print ('%d:  rho_t = %f,  held-out perplexity estimate = %f' % \
            (iteration, olda._rhot, numpy.exp(-perwordbound)))

        # Save lambda, the parameters to the variational distributions
        # over topics, and gamma, the parameters to the variational
        # distributions over topic weights for the text files analyzed in
        # the last iteration.
        if (iteration % 10 == 0):
            numpy.savetxt('parameters/lambda-%d.dat' % iteration, olda._lambda)
            numpy.savetxt('parameters/gamma-%d.dat' % iteration, gamma)

if __name__ == '__main__':
    main()
