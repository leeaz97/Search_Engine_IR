import re

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

    #def add_idf(self,num_doc):
    #    for k, v in self.inverted_idx.items():
    #        self.inverted_idx[k] = (v, math.log10(num_doc/v))


    def sorted_inverted(self):
        #sort by key
        dict(sorted(self.inverted_idx.items()))
        #sort by val
        #sorted( self.inverted_idx.items(), key=lambda x: x[1])



    def sorted_posting(self,term,post_file):
        # sort the posting by tweet_id
        if post_file == "A-Fa-f":
            sorted(self.postingDictAF[term], key=lambda x: x[0])
        elif post_file == "G-Pg-p":
            sorted(self.postingDictGP[term], key=lambda x: x[0])
        elif post_file == "Q-Zq-z":
            sorted(self.postingDictQZ[term], key=lambda x: x[0])
        elif post_file == "Simbol":
            sorted(self.postingDictSimbol[term], key=lambda x: x[0])

    def posting_by_FirstChar(self,term):#,pos):
        if re.match(r'^[A-Fa-f]', term):
            return "A-Fa-f"
        elif re.match(r'^[G-Pg-p]', term):
            return "G-Pg-p"
        elif re.match(r'^[Q-Zq-z]', term):
            return "Q-Zq-z"
        else:
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
            try:
                if term.lower() == "anthoni":
                    print(term)
                    #print( self.postingDictGP[term])
                    #print( self.postingDictGPpterm[term[0]+term[1]])
                #continue if the term empty
                if term =='':
                    continue
                #there is non meaning to one char so ont index thim
                if len(term) == 1:
                    continue

                post_file = self.posting_by_FirstChar(term)
                pos = (document.tweet_id, document_dictionary[term],
                                  document.doc_length,
                                  document_dictionary[term] / document.max_tf,
                                  document.max_tf,document.nf,document.tweet_date,list(document_dictionary.keys()))

                # if the term Start with Upper
                if term[0].isupper():
                    # if its start with upper and exists as lower in the inverted indexer
                    if term.lower() in self.inverted_idx.keys():
                        self.inverted_idx[term.lower()] += 1

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
                        self.inverted_idx[term] = 1
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

                    else:
                        # if its start with upper and exists in the inverted indexer
                        self.inverted_idx[term] += 1

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
                        # sort the posting by tweet_id
                        self.sorted_posting(term, post_file)

                else:
                    # if the term Start with Lower and exists as First charchter Upper in the inverted indexer,remove from the inverted index and postingfile
                    if term[0].upper()+term[1:] in self.inverted_idx.keys() and re.match('[a-z]',term[0]):
                        inv_data = self.inverted_idx.pop(term[0].upper() + term[1:])
                        self.inverted_idx[term] = inv_data + 1

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

                        # sort the posting by tweet_id
                        self.sorted_posting(term, post_file)

                    # if the term Start with Lower or digit or #@$ and not exists in the inverted indexer
                    elif term not in self.inverted_idx.keys():
                            self.inverted_idx[term] = 1

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

                    else:
                        # if its start with Lower and exists in the inverted indexer
                        self.inverted_idx[term] += 1

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

            except:
                print('problem with the following key {}'.format(term))
