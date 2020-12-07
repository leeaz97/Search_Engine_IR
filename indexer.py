import re

class Indexer:

    def __init__(self, config):
        self.inverted_idx = {}
        self.postingDictTOI = {}
        self.postingDictSWC = {}
        self.postingDictBPH = {}
        self.postingDictFMD = {}
        self.postingDictREL = {}
        self.postingDictNAG = {}
        self.postingDictUKVY = {}
        self.postingDictJQZX = {}
        self.postingDictNum = {}
        self.postingDictHashtag = {}
        self.postingDictStrudel = {}
        self.postingDictSimbol = {}
        self.document_collection = {}
        self.postingEntities = {}
        self.inverted_idxEntities = {}
        self.config = config

    def init_posting(self):
        self.inverted_idx = {}
        self.postingDictTOI = {}
        self.postingDictSWC = {}
        self.postingDictBPH = {}
        self.postingDictFMD = {}
        self.postingDictREL = {}
        self.postingDictNAG = {}
        self.postingDictUKVY = {}
        self.postingDictJQZX = {}
        self.postingDictNum = {}
        self.postingDictHashtag = {}
        self.postingDictStrudel = {}
        self.postingDictSimbol = {}
        self.document_collection = {}

    def remove_uniqe_entities(self):
        for k,v in self.inverted_idxEntities.items():
            if v ==1 :
                self.inverted_idxEntities.pop(k)
                self.postingEntities.pop(k.lower())


    def posting(self,term,doc_details):

        if re.match(r'^[TOItoi]', term):
            if term.lower() not in self.postingDictTOI.keys():
                self.postingDictTOI[term.lower()] = [doc_details]
            else:
                self.postingDictTOI[term.lower()].append(doc_details)

        elif re.match(r'^[SWCswc]', term):
            if term.lower() not in self.postingDictSWC.keys():
                self.postingDictSWC[term.lower()] = [doc_details]
            else:
                self.postingDictSWC[term.lower()].append(doc_details)

        elif re.match(r'^[BPHbph]', term):
            if term.lower() not in self.postingDictBPH.keys():
                self.postingDictBPH[term.lower()] = [doc_details]
            else:
                self.postingDictBPH[term.lower()].append(doc_details)

        elif re.match(r'^[FMDtmd]', term):
            if term.lower() not in self.postingDictFMD.keys():
                self.postingDictFMD[term.lower()] = [doc_details]
            else:
                self.postingDictFMD[term.lower()].append(doc_details)

        elif re.match(r'^[RELrel]', term):
            if term.lower() not in self.postingDictREL.keys():
                self.postingDictREL[term.lower()] = [doc_details]
            else:
                self.postingDictREL[term.lower()].append(doc_details)

        elif re.match(r'^[NAGnag]', term):
            if term.lower() not in self.postingDictNAG.keys():
                self.postingDictNAG[term.lower()] = [doc_details]
            else:
                self.postingDictNAG[term.lower()].append(doc_details)

        elif re.match(r'^[UKVYukvy]', term):
            if term.lower() not in self.postingDictUKVY.keys():
                self.postingDictUKVY[term.lower()] = [doc_details]
            else:
                self.postingDictUKVY[term.lower()].append(doc_details)

        elif re.match(r'^[JQZXjqzx]', term):
            if term.lower() not in self.postingDictJQZX.keys():
                self.postingDictJQZX[term.lower()] = [doc_details]
            else:
                self.postingDictJQZX[term.lower()].append(doc_details)

        elif re.match(r'^[0-9]', term):
            if term.lower() not in self.postingDictNum.keys():
                self.postingDictNum[term.lower()] = [doc_details]
            else:
                self.postingDictNum[term.lower()].append(doc_details)

        elif re.match(r'^#', term):
            if term.lower() not in self.postingDictHashtag.keys():
                self.postingDictHashtag[term.lower()] = [doc_details]
            else:
                self.postingDictHashtag[term.lower()].append(doc_details)

        elif re.match(r'^@', term):
            if term.lower() not in self.postingDictStrudel.keys():
                self.postingDictStrudel[term.lower()] = [doc_details]
            else:
                self.postingDictStrudel[term.lower()].append(doc_details)

        else: #Simbol
            if term.lower() not in self.postingDictSimbol.keys():
                self.postingDictSimbol[term.lower()] = [doc_details]
            else:
                self.postingDictSimbol[term.lower()].append(doc_details)


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
                # continue if the term empty
                if term.lower() in ['', 'rt', 'https', 'co']:
                    continue

                #there is non meaning to one char so ont index thim
                if len(term) == 1:
                    continue

                #post_file = self.posting_by_FirstChar(term)
                doc_details = (document.tweet_id, document_dictionary[term],
                                  document.doc_length,
                                  document.max_tf,document.nf,document.tweet_date) #,list(document_dictionary.keys()))


                if document.tweet_id not in self.document_collection.keys():
                    self.document_collection[document.tweet_id] = document_dictionary

                # if the term Start with Upper
                if term[0].isupper():
                    # if its start with upper and exists as lower in the inverted indexer
                    if term.lower() in self.inverted_idx.keys():
                        self.inverted_idx[term.lower()] += 1
                        self.posting(term,doc_details)

                        #if post_file == "A-Fa-f":
                        #    if term.lower() not in self.postingDictAF.keys():
                        #        self.postingDictAF[term.lower()] = [pos]
                        #    else:
                        #        self.postingDictAF[term.lower()].append(pos)
                        #elif post_file == "G-Pg-p":
                        #    if term.lower() not in self.postingDictGP.keys():
                        #        self.postingDictGP[term.lower()] = [pos]
                        #    else:
                        #        self.postingDictGP[term.lower()].append(pos)
                        #elif post_file == "Q-Zq-z":
                        #    if term.lower() not in self.postingDictQZ.keys():
                        #        self.postingDictQZ[term.lower()] = [pos]
                        #    else:
                        #        self.postingDictQZ[term.lower()].append(pos)
                        #elif post_file == "Simbol":
                        #    if term.lower() not in self.postingDictSimbol.keys():
                        #        self.postingDictSimbol[term.lower()] = [pos]
                        #    else:
                        #        self.postingDictSimbol[term.lower()].append(pos)
                        #sort the posting by tweet_id

                    # if its start with upper and not exists in the inverted indexer
                    elif term not in self.inverted_idx.keys():
                        self.inverted_idx[term] = 1
                        self.posting(term, doc_details)
                        # if new in index new in posting
                        #if post_file == "A-Fa-f":
                            #self.postingDictAF[term] = [pos]
                        #    self.postingDictAF[term.lower()] = [pos]
                        #elif post_file == "G-Pg-p":
                            #self.postingDictGP[term] = [pos]
                        #    self.postingDictGP[term.lower()] = [pos]
                        #elif post_file == "Q-Zq-z":
                            #self.postingDictQZ[term] = [pos]
                        #    self.postingDictQZ[term.lower()] = [pos]
                        #elif post_file == "Simbol":
                            #self.postingDictSimbol[term] = [pos]
                         #   self.postingDictSimbol[term.lower()] = [pos]

                        # sort the posting by tweet_id
                        #self.sorted_posting(term, post_file)

                    else:
                        # if its start with upper and exists in the inverted indexer
                        self.inverted_idx[term] += 1
                        self.posting(term, doc_details)
                        #if post_file == "A-Fa-f":
                        #    if term.lower() not in self.postingDictAF.keys():
                                #self.postingDictAF[term] = [pos]
                        #        self.postingDictAF[term.lower()] = [pos]
                        #    else:
                                #self.postingDictAF[term].append(pos)
                        #        self.postingDictAF[term.lower()].append(pos)
                        #elif post_file == "G-Pg-p":
                            #if term.lower() not in self.postingDictGP.keys():
                                #self.postingDictGP[term] = [pos]
                             #   self.postingDictGP[term.lower()] = [pos]
                            #else:
                                #self.postingDictGP[term].append(pos)
                            #    self.postingDictGP[term.lower()].append(pos)
                        #elif post_file == "Q-Zq-z":
                        #    if term.lower() not in self.postingDictQZ.keys():
                                #self.postingDictQZ[term] = [pos]
                        #        self.postingDictQZ[term.lower()] = [pos]
                        #    else:
                                #self.postingDictQZ[term].append(pos)
                        #        self.postingDictQZ[term.lower()].append(pos)
                        #elif post_file == "Simbol":
                        #    if term.lower() not in self.postingDictSimbol.keys():
                                #self.postingDictSimbol[term] = [pos]
                        #        self.postingDictSimbol[term.lower()] = [pos]
                        #    else:
                                #self.postingDictSimbol[term].append(pos)
                        #        self.postingDictSimbol[term.lower()].append(pos)

                else:
                    # if the term Start with Lower and exists as First charchter Upper in the inverted indexer,remove from the inverted index and postingfile
                    if term[0].upper()+term[1:] in self.inverted_idx.keys() and re.match('[a-z]',term[0]):
                        inv_data = self.inverted_idx.pop(term[0].upper() + term[1:])
                        self.inverted_idx[term] = inv_data + 1
                        self.posting(term, doc_details)
                        #if post_file == "A-Fa-f":
                            #if term[0].upper()+term[1:] in self.postingDictAF.keys():
                            #    self.postingDictAF[term] = []
                            #    temp = self.postingDictAF.pop(term[0].upper()+term[1:])
                            #    for i in temp:
                            #        self.postingDictAF[term].append(i)
                            #    self.postingDictAF[term].append(pos)
                            #else:
                            #    self.postingDictAF[term] = [pos]
                            #if term.lower() not in self.postingDictAF.keys():
                            #    self.postingDictAF[term.lower()] = [pos]
                            #else:
                            #    self.postingDictAF[term.lower()].append(pos)

                        #elif post_file == "G-Pg-p":
                            #if term[0].upper()+term[1:]  in self.postingDictGP.keys():
                            #    self.postingDictGP[term] = []
                            #    temp = self.postingDictGP.pop(term[0].upper() + term[1:])
                            #    for i in temp:
                            #        self.postingDictGP[term].append(i)
                            #    self.postingDictGP[term].append(pos)
                            #else:
                            #    self.postingDictGP[term] = [pos]
                            #if term.lower() not in self.postingDictGP.keys():
                            #    self.postingDictGP[term.lower()] = [pos]
                            #else:
                            #    self.postingDictGP[term.lower()].append(pos)

                        #elif post_file == "Q-Zq-z":
                            #if term[0].upper()+term[1:] in self.postingDictQZ.keys():
                            #    self.postingDictQZ[term] = []
                            #    temp = self.postingDictQZ.pop(term[0].upper() + term[1:])
                            #    for i in temp:
                            #        self.postingDictQZ[term].append(i)
                            #    self.postingDictQZ[term].append(pos)
                            #else:
                            #    self.postingDictQZ[term] = [pos]
                            #if term.lower() not in self.postingDictQZ.keys():
                            #    self.postingDictQZ[term.lower()] = [pos]
                            #else:
                            #    self.postingDictQZ[term.lower()].append(pos)

                        #elif post_file == "Simbol":
                            #if term[0].upper()+term[1:]  in self.postingDictSimbol.keys():
                            #    self.postingDictSimbol[term] = []
                            #    temp = self.postingDictSimbol.pop(term[0].upper() + term[1:])
                            #    for i in temp:
                            #        self.postingDictSimbol[term].append(i)
                            #    self.postingDictSimbol[term].append(pos)
                            #else:
                            #    self.postingDictSimbol[term] = [pos]
                            #if term.lower() not in self.postingDictSimbol.keys():
                            #    self.postingDictSimbol[term.lower()] = [pos]
                            #else:
                            #    self.postingDictSimbol[term.lower()].append(pos)


                    # if the term Start with Lower or digit or #@$ and not exists in the inverted indexer
                    elif term not in self.inverted_idx.keys():
                            self.inverted_idx[term] = 1
                            self.posting(term, doc_details)
                            #if post_file == "A-Fa-f":
                                #self.postingDictAF[term] = [pos]
                                #self.postingDictAF[term.lower()] = [pos]
                            #elif post_file == "G-Pg-p":
                                #self.postingDictGP[term] = [pos]
                            #    self.postingDictGP[term.lower()] = [pos]
                            #elif post_file == "Q-Zq-z":
                                #self.postingDictQZ[term] = [pos]
                            #    self.postingDictQZ[term.lower()] = [pos]
                            #elif post_file == "Simbol":
                                #self.postingDictSimbol[term] = [pos]
                            #    self.postingDictSimbol[term.lower()] = [pos]

                    else:
                        # if its start with Lower and exists in the inverted indexer
                        self.inverted_idx[term] += 1
                        self.posting(term, doc_details)
                        #if post_file == "A-Fa-f":
                        #    if term.lower() not in self.postingDictAF.keys():
                        #        #self.postingDictAF[term] = [pos]
                        #        self.postingDictAF[term.lower()] = [pos]
                        #    else:
                                #self.postingDictAF[term].append(pos)
                        #        self.postingDictAF[term.lower()].append(pos)
                        #elif post_file == "G-Pg-p":
                        #    if term.lower() not in self.postingDictGP.keys():
                                #self.postingDictGP[term] = [pos]
                        #        self.postingDictGP[term.lower()] = [pos]
                        #    else:
                                #self.postingDictGP[term].append(pos)
                        #        self.postingDictGP[term.lower()].append(pos)
                        #elif post_file == "Q-Zq-z":
                        #    if term.lower() not in self.postingDictQZ.keys():
                                #self.postingDictQZ[term] = [pos]
                        #        self.postingDictQZ[term.lower()] = [pos]
                        #    else:
                                #self.postingDictQZ[term].append(pos)
                        #        self.postingDictQZ[term.lower()].append(pos)
                        #elif post_file == "Simbol":
                        #    if term.lower() not in self.postingDictSimbol.keys():
                                #self.postingDictSimbol[term] = [pos]
                         #       self.postingDictSimbol[term.lower()] = [pos]
                         #   else:
                                #self.postingDictSimbol[term].append(pos)
                         #       self.postingDictSimbol[term.lower()].append(pos)

                        # sort the posting by tweet_id
                        #self.sorted_posting(term, post_file)
            except:
                print('problem with the following key {}'.format(term))

        for e in document.entities:
            if e in self.inverted_idxEntities:
                self.inverted_idx[e]+=1
                self.postingEntities[e].append((document.tweet_id, document_dictionary[term],
                                  document.doc_length,
                                  document.max_tf,document.nf,document.tweet_date))
            else:
                self.inverted_idx[e] = 1
                self.postingEntities[e] = [(document.tweet_id, document_dictionary[term],
                                  document.doc_length,
                                  document.max_tf,document.nf,document.tweet_date)]

