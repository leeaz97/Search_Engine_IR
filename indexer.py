import re
from postingData import PostingData
from invertedData import InvertedData
class Indexer:

    def __init__(self, config):
        self.inverted_idx = {}
        self.postingDictAF = {}
        self.postingDictGP = {}
        self.postingDictQZ = {}
        self.postingDictSimbol = {}
        self.config = config

    def init_posting(self):
        self.postingDictAF = {}
        self.postingDictGP = {}
        self.postingDictQZ = {}
        self.postingDictSimbol = {}

    def sorted_inverted(self):
        sorted( self.inverted_idx.items(), key=lambda x: x[1])

    def sorted_posting(self,term,post_file):
        # sort the posting by tweet_id
        if post_file == "A-Fa-f":
            sorted(self.postingDictAF[term], key=lambda x: x[0])
        #    #self.postingDict[term].sort()
        elif post_file == "G-Pg-p":
            sorted(self.postingDictGP[term], key=lambda x: x[0])
        #    #self.postingDictGP[term].sort()
        elif post_file == "Q-Zq-z":
            sorted(self.postingDictQZ[term], key=lambda x: x[0])
        #    #self.postingDictQZ[term].sort()
        elif post_file == "Simbol":
            sorted(self.postingDictSimbol[term], key=lambda x: x[0])
        #    #self.postingDictSimbol[term].sort()

    def posting_by_FirstChar(self,term):#,pos):
        if re.match(r'^[A-Fa-f]', term):
            #self.postingDictAF[term].append(pos)
            return "A-Fa-f"
        elif re.match(r'^[G-Pg-p]', term):
            #self.postingDictGP[term].append(pos)
            return "G-Pg-p"
        elif re.match(r'^[Q-Zq-z]', term):
            #self.postingDictQZ[term].append(pos)
            return "Q-Zq-z"
        else:
            #self.postingSimbol[term].append(pos)
            return "Simbol"

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
            # Update inverted index and posting
            try:
                #continue if the term empty
                if term =='':
                    continue

                post_file = self.posting_by_FirstChar(term)
                pos = (document.tweet_id, document_dictionary[term],
                                  document.doc_length,
                                  document_dictionary[term] / document.max_tf,
                                  document.max_tf, document.tweet_date)

                #invert_data= InvertedData(0,[])
                # if the term Start with Upper
                if term[0].isupper():
                    # if its start with upper and exists as lower in the inverted indexer
                    if term.lower() in self.inverted_idx.keys():
                        self.inverted_idx[term.lower()] += 1
                        #self.inverted_idx[term.lower()].postingfile_list.append(post_file)

                        if post_file == "A-Fa-f":
                            self.postingDictAF[term.lower()].append(pos)
                        elif post_file == "G-Pg-p":
                            self.postingDictGP[term.lower()].append(pos)
                        elif post_file == "Q-Zq-z":
                            self.postingDictQZ[term.lower()].append(pos)
                        elif post_file == "Simbol":
                            self.postingDictSimbol[term.lower()].append(pos)
                        #sort the posting by tweet_id
                        self.sorted_posting(term.lower(),post_file)

                        # if its start with upper and not exists in the inverted indexer
                    elif term not in self.inverted_idx.keys():
                        #self.inverted_idx[term] = invert_data
                        self.inverted_idx[term] = 1
                        #self.inverted_idx[term].postingfile_list.append(post_file)

                        if post_file == "A-Fa-f":
                            self.postingDictAF[term] = [pos]
                        elif post_file == "G-Pg-p":
                            self.postingDictGP[term] = [pos]
                        elif post_file == "Q-Zq-z":
                            self.postingDictQZ[term] = [pos]
                        elif post_file == "Simbol":
                            self.postingDictSimbol[term] = [pos]

                        # sort the posting by tweet_id
                        self.sorted_posting(term, post_file)

                        #self.postingDict[term].append((document.tweet_id, document_dictionary[term],
                        #                               document.doc_length,
                        #                               document_dictionary[term] / document.max_tf,
                        #                               document.max_tf, document.tweet_date))


                    else:
                        # if its start with upper and exists in the inverted indexer
                        self.inverted_idx[term] += 1
                        #self.inverted_idx[term].postingfile_list.append(post_file)
                        if post_file == "A-Fa-f":
                            self.postingDictAF[term].append(pos)
                        elif post_file == "G-Pg-p":
                            self.postingDictGP[term].append(pos)
                        elif post_file == "Q-Zq-z":
                            self.postingDictQZ[term].append(pos)
                        elif post_file == "Simbol":
                            self.postingDictSimbol[term].append(pos)
                        #self.postingDict[term].append(pos)
                        # sort the posting by tweet_id
                        self.sorted_posting(term, post_file)
                    #tweer id,tf,len doc,tf_normal,max_term,tweet date
                    #self.postingDict[term.lower()].append((document.tweet_id,document_dictionary[term],document.doc_length,document_dictionary[term]/document.max_tf,document.max_tf,document.tweet_date))
                else:
                        # if the term Start with Lower and exists as First charchter Upper in the inverted indexer,remove from the inverted index and postingfile
                    if term[0].upper()+term[1:] in self.inverted_idx.keys() and re.match('[a-z]',term[0]):
                        inv_data = self.inverted_idx.pop(term[0].upper() + term[1:])
                        #self.inverted_idx[term] = invert_data
                        self.inverted_idx[term] = inv_data + 1
                        #self.inverted_idx[term].postingfile_list.append(post_file)
                        if post_file == "A-Fa-f":
                            self.postingDictAF[term] = []
                            temp = self.postingDictAF.pop(term[0].upper()+term[1:])
                            for i in temp:
                                self.postingDictAF[term].append(i)
                            self.postingDictAF[term].append(pos)
                        elif post_file == "G-Pg-p":
                            self.postingDictGP[term] = []
                            temp = self.postingDictGP.pop(term[0].upper() + term[1:])
                            for i in temp:
                                self.postingDictGP[term].append(i)
                            self.postingDictGP[term].append(pos)
                        elif post_file == "Q-Zq-z":
                            self.postingDictQZ[term] = []
                            temp = self.postingDictQZ.pop(term[0].upper() + term[1:])
                            for i in temp:
                                self.postingDictQZ[term].append(i)
                            self.postingDictQZ[term].append(pos)
                        elif post_file == "Simbol":
                            self.postingDictSimbol[term] = []
                            temp = self.postingDictSimbol.pop(term[0].upper() + term[1:])
                            for i in temp:
                                self.postingDictSimbol[term].append(i)
                            self.postingDictSimbol[term].append(pos)

                            #print(self.postingDict[term])
                        # sort the posting by tweet_id
                        self.sorted_posting(term, post_file)
                        # if the term Start with Lower or digit or #@$ and not exists in the inverted indexer
                    elif term not in self.inverted_idx.keys():
                            #self.inverted_idx[term] = invert_data
                            self.inverted_idx[term] = 1
                            #self.inverted_idx[term].postingfile_list.append(post_file)

                            if post_file == "A-Fa-f":
                                self.postingDictAF[term] = [pos]
                            elif post_file == "G-Pg-p":
                                self.postingDictGP[term] = [pos]
                            elif post_file == "Q-Zq-z":
                                self.postingDictQZ[term] = [pos]
                            elif post_file == "Simbol":
                                self.postingDictSimbol[term] = [pos]

                            # sort the posting by tweet_id
                            self.sorted_posting(term, post_file)
                            #self.postingDict[term].append((document.tweet_id, document_dictionary[term],
                            #                                       document.doc_length,
                            #                                       document_dictionary[term] / document.max_tf,
                            #                                       document.max_tf, document.tweet_date))
                    else:
                        # if its start with Lower and exists in the inverted indexer
                        self.inverted_idx[term] += 1
                        #self.inverted_idx[term].postingfile_list.append(post_file)
                        if post_file == "A-Fa-f":
                            self.postingDictAF[term].append(pos)
                        elif post_file == "G-Pg-p":
                            self.postingDictGP[term].append(pos)
                        elif post_file == "Q-Zq-z":
                            self.postingDictQZ[term].append(pos)
                        elif post_file == "Simbol":
                            self.postingDictSimbol[term].append(pos)

                        # sort the posting by tweet_id
                        self.sorted_posting(term, post_file)



            except:
                #print(self.inverted_idx)
                #print(self.postingDictGP)
                print('problem with the following key {}'.format(term))
