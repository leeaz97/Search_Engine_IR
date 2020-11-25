import re
class Indexer:

    def __init__(self, config):
        self.inverted_idx = {}
        self.postingDict = {}
        self.config = config


    def add_new_doc(self, document):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """

        document_dictionary = document.term_doc_dictionary
        # Go over each term in the doc
        for term in document_dictionary.keys():
            try:
                # Update inverted index and posting
                # caculate the df
                #if the term Start with Upper

                if term[0].isupper():
                    # if its start with upper and exists as lower in the inverted indexer
                    if term.lower() in self.inverted_idx.keys():
                        self.inverted_idx[term.lower()] += 1
                        self.postingDict[term.lower()].append((document.tweet_id, document_dictionary[term],
                                                               document.doc_length,
                                                               document_dictionary[term] / document.max_tf,
                                                               document.max_tf, document.tweet_date))

                        # if its start with upper and not exists in the inverted indexer
                    elif term not in self.inverted_idx.keys():
                        self.inverted_idx[term] = 1
                        self.postingDict[term] = []
                        self.postingDict[term].append((document.tweet_id, document_dictionary[term],
                                                       document.doc_length,
                                                       document_dictionary[term] / document.max_tf,
                                                       document.max_tf, document.tweet_date))

                    else:
                        # if its start with upper and exists in the inverted indexer
                        self.inverted_idx[term] += 1
                        self.postingDict[term].append((document.tweet_id, document_dictionary[term],
                                                               document.doc_length,
                                                               document_dictionary[term] / document.max_tf,
                                                               document.max_tf, document.tweet_date))

                    #tweer id,tf,len doc,tf_normal,max_term,tweet date
                    #self.postingDict[term.lower()].append((document.tweet_id,document_dictionary[term],document.doc_length,document_dictionary[term]/document.max_tf,document.max_tf,document.tweet_date))
                else:
                        # if the term Start with Lower and exists as First charchter Upper in the inverted indexer,remove from the inverted index and postingfile
                    if term[0].upper()+term[1:] in self.inverted_idx.keys() and re.match('[a-z]',term[0]):
                            self.inverted_idx[term] = self.inverted_idx.pop(term[0].upper()+term[1:]) + 1
                            #print(self.inverted_idx[term])
                            self.postingDict[term] = []
                            temp = self.postingDict.pop(term[0].upper()+term[1:])
                            for i in temp:
                                self.postingDict[term].append(i)
                            self.postingDict[term].append((document.tweet_id, document_dictionary[term],
                                                                   document.doc_length,
                                                                   document_dictionary[term] / document.max_tf,
                                                                   document.max_tf, document.tweet_date))
                            #print(self.postingDict[term])

                        # if the term Start with Lower or digit or #@$ and not exists in the inverted indexer
                    elif term not in self.inverted_idx.keys():
                            self.inverted_idx[term] = 1
                            self.postingDict[term] = []
                            self.postingDict[term].append((document.tweet_id, document_dictionary[term],
                                                                   document.doc_length,
                                                                   document_dictionary[term] / document.max_tf,
                                                                   document.max_tf, document.tweet_date))
                    else:
                        # if its start with Lower and exists in the inverted indexer
                        self.inverted_idx[term] += 1
                        self.postingDict[term].append((document.tweet_id, document_dictionary[term],
                                                                   document.doc_length,
                                                                   document_dictionary[term] / document.max_tf,
                                                                   document.max_tf, document.tweet_date))

            except:
                print('problem with the following key {}'.format(term))
