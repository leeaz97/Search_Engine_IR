import re
import math
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

    def add_idf(self,num_doc):
        for k, v in self.inverted_idx.items():
            self.inverted_idx[k] = (v, math.log10(num_doc/v))


    def sorted_inverted(self):
        #sort by key
        dict(sorted(self.inverted_idx.items()))
        #sort by val
        #sorted( self.inverted_idx.items(), key=lambda x: x[1])



    def sorted_posting(self,term,post_file):
        # sort the posting by tweet_id
        if post_file == "A-Fa-f":
            #self.postingDictAF = sorted_dic_by_listval(self.postingDictAF,term)
            sorted(self.postingDictAF[term], key=lambda x: x[0])
        elif post_file == "G-Pg-p":
            #self.postingDictGP = sorted_dic_by_listval(self.postingDictGP, term)
            sorted(self.postingDictGP[term], key=lambda x: x[0])
        elif post_file == "Q-Zq-z":
            #self.postingDictQZ = sorted_dic_by_listval(self.postingDictQZ, term)
            sorted(self.postingDictQZ[term], key=lambda x: x[0])
        elif post_file == "Simbol":
            #self.postingDictSimbol = sorted_dic_by_listval(self.postingDictSimbol, term)
            sorted(self.postingDictSimbol[term], key=lambda x: x[0])

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
                                  document.max_tf , document.nf, document.tweet_date)

                #invert_data= InvertedData(0,[])
                # if the term Start with Upper
                if term[0].isupper():
                    # if its start with upper and exists as lower in the inverted indexer
                    if term.lower() in self.inverted_idx.keys():
                        self.inverted_idx[term.lower()] += 1
                        #self.inverted_idx[term.lower()].postingfile_list.append(post_file)

                        if post_file == "A-Fa-f":
                            if term.lower() not in self.postingDictAF.keys():
                                self.postingDictAF[term.lower()] = [pos]
                            else:
                                self.postingDictAF[term.lower()].append(pos)
                        elif post_file == "G-Pg-p":
                            if term.lower() not in self.postingDictGP.keys():
                                self.postingDictGP[term.lower()] = [pos]
                            else:
                                self.postingDictGP[term.lower()].append(pos)
                        elif post_file == "Q-Zq-z":
                            if term.lower() not in self.postingDictQZ.keys():
                                self.postingDictQZ[term.lower()] = [pos]
                            else:
                                self.postingDictQZ[term.lower()].append(pos)
                        elif post_file == "Simbol":
                            if term.lower() not in self.postingDictSimbol.keys():
                                self.postingDictSimbol[term.lower()] = [pos]
                            else:
                                self.postingDictSimbol[term.lower()].append(pos)
                        #sort the posting by tweet_id
                        self.sorted_posting(term.lower(),post_file)

                    #if term[0].lower()+term[1:] in self.inverted_idx.keys():
                        #self.inverted_idx[term[0].lower()+term[1:]] += 1
                        #if post_file == "A-Fa-f":
                         #   if term[0].lower()+term[1:] not in self.postingDictAF.keys():
                         #       self.postingDictAF[term[0].lower()+term[1:] ] = [pos]
                         #   else:
                         #       self.postingDictAF[term[0].lower()+term[1:] ].append(pos)
                        #elif post_file == "G-Pg-p":
                        #    if term[0].lower()+term[1:] not in self.postingDictGP.keys():
                        #        self.postingDictGP[term[0].lower()+term[1:] ] = [pos]
                        #    else:
                        #        self.postingDictGP[term[0].lower()+term[1:] ].append(pos)
                        #elif post_file == "Q-Zq-z":
                        #    if term[0].lower()+term[1:] not in self.postingDictQZ.keys():
                        #        self.postingDictQZ[term[0].lower()+term[1:] ] = [pos]
                        #    else:
                        #        self.postingDictQZ[term[0].lower()+term[1:] ].append(pos)
                        #elif post_file == "Simbol":
                        #    if term[0].lower()+term[1:] not in self.postingDictSimbol.keys():
                        #        self.postingDictSimbol[term[0].lower()+term[1:] ] = [pos]
                        #    else:
                        #        self.postingDictSimbol[term[0].lower()+term[1:] ].append(pos)
                        #sort the posting by tweet_id
                        #self.sorted_posting(term[0].lower()+term[1:] ,post_file)

                    # if its start with upper and not exists in the inverted indexer
                    elif term not in self.inverted_idx.keys():
                        #self.inverted_idx[term] = invert_data
                        self.inverted_idx[term] = 1
                        #self.inverted_idx[term].postingfile_list.append(post_file)
                        # if new in index new in posting
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
                            if term not in self.postingDictAF.keys():
                                self.postingDictAF[term] = [pos]
                            else:
                                self.postingDictAF[term].append(pos)
                        elif post_file == "G-Pg-p":
                            if term not in self.postingDictGP.keys():
                                self.postingDictGP[term] = [pos]
                            else:
                                self.postingDictGP[term].append(pos)
                        elif post_file == "Q-Zq-z":
                            if term not in self.postingDictQZ.keys():
                                self.postingDictQZ[term] = [pos]
                            else:
                                self.postingDictQZ[term].append(pos)
                        elif post_file == "Simbol":
                            if term not in self.postingDictSimbol.keys():
                                self.postingDictSimbol[term] = []
                            else:
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
                        self.inverted_idx[term] = inv_data + 1
                        #self.inverted_idx[term].postingfile_list.append(post_file)
                        if post_file == "A-Fa-f":
                            if term[0].upper()+term[1:] in self.postingDictAF.keys():
                                self.postingDictAF[term] = []
                                temp = self.postingDictAF.pop(term[0].upper()+term[1:])
                                for i in temp:
                                    self.postingDictAF[term].append(i)
                                self.postingDictAF[term].append(pos)
                            else:
                                self.postingDictAF[term] = [pos]

                        elif post_file == "G-Pg-p":
                            if term[0].upper()+term[1:]  in self.postingDictGP.keys():
                                self.postingDictGP[term] = []
                                temp = self.postingDictGP.pop(term[0].upper() + term[1:])
                                for i in temp:
                                    self.postingDictGP[term].append(i)
                                self.postingDictGP[term].append(pos)
                            else:
                                self.postingDictGP[term] = [pos]

                        elif post_file == "Q-Zq-z":
                            if term[0].upper()+term[1:] in self.postingDictQZ.keys():
                                self.postingDictQZ[term] = []
                                temp = self.postingDictQZ.pop(term[0].upper() + term[1:])
                                for i in temp:
                                    self.postingDictQZ[term].append(i)
                                self.postingDictQZ[term].append(pos)
                            else:
                                self.postingDictQZ[term] = [pos]

                        elif post_file == "Simbol":
                            if term[0].upper()+term[1:]  in self.postingDictSimbol.keys():
                                self.postingDictSimbol[term] = []
                                temp = self.postingDictSimbol.pop(term[0].upper() + term[1:])
                                for i in temp:
                                    self.postingDictSimbol[term].append(i)
                                self.postingDictSimbol[term].append(pos)
                            else:
                                self.postingDictSimbol[term] = [pos]

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
                            if term not in self.postingDictAF.keys():
                                self.postingDictAF[term] = [pos]
                            else:
                                self.postingDictAF[term].append(pos)
                        elif post_file == "G-Pg-p":
                            if term not in self.postingDictGP.keys():
                                self.postingDictGP[term] = [pos]
                            else:
                                self.postingDictGP[term].append(pos)
                        elif post_file == "Q-Zq-z":
                            if term not in self.postingDictQZ.keys():
                                self.postingDictQZ[term] = [pos]
                            else:
                                self.postingDictQZ[term].append(pos)
                        elif post_file == "Simbol":
                            if term not in self.postingDictSimbol.keys():
                                self.postingDictSimbol[term] = [pos]
                            else:
                                self.postingDictSimbol[term].append(pos)

                        # sort the posting by tweet_id
                        self.sorted_posting(term, post_file)
                        #self.sorted_inverted()



            except:
                #print(self.inverted_idx)
                #print(self.postingDictGP)
                print('problem with the following key {}'.format(term))
