from parser_module import Parse
from ranker import Ranker
from ReleventDoc import ReleventDocData
import utils
import re
import os
import math
from stemmer import Stemmer

from gensim.models import KeyedVectors
import numpy as np


def splitLst(x):
    dictionary = dict()
    for word in x:
        f = word[0]
        if f in dictionary.keys():
            dictionary[f].append(word)
        else:
            dictionary[f] = [word]
    return dictionary

class Searcher:

    def __init__(self, inverted_index,document_collection,config):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse(config)
        self.ranker = Ranker()
        self.inverted_index = inverted_index
        self.document_collection = document_collection
        self.stemming = config.toStem
        self.outputPath = config.get__outputPath()
        self.corpus_num_docs = config.number_of_documents
        self.posting_doc = {}

    def avg_vector(self,doc_list_key,model):
        np_arry = np.zeros(300, )
        num_vec = 0
        for term in doc_list_key:
            if term in model.vocab:
                np_arry = np.add(np_arry, model.wv[term])
                num_vec += 1
        if num_vec > 0:
            return np.true_divide(np_arry, num_vec)
        else:
            return np_arry

    def freq_terms_query(self,list_query):
        term_dict = {}
        for term in list_query:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        max_tf = max(term_dict.values())

        # normal the query with the tf of the most common term
        for k,v in term_dict.items():
            term_dict[k] = term_dict[k]/max_tf

        return term_dict

    def expend_query_w2v(self,w2v_model,query_list,top=5):
        exp = []
        for word in query_list:
            if word in w2v_model.vocab:
                result = w2v_model.most_similar(positive=[word], topn=top)
                for i in range(top):
                    if result[i][1] >= 0.8:
                        #add to exp the word that 80% similar
                        exp.append(result[i][0])
        return list(set(exp))

    #def term_in_inve(self,term,k):
    #    if term in k:
    #        return (True,term)
    #    if term.lower() in k:
    #        return (True,term.lower())
    #    if term.upper() in k:
    #        return (True,term.upper())
    #    if term[0].lower()+term[1:] in k:
    #        return (True,term[0].lower()+term[1:])
    #    if term[0].upper()+term[1:] in k:
    #        return (True,term[0].upper()+term[1:])
    #    return (False, '')


    def load_posting(self,chr,list_word):
        if re.match(r'^[TOItoi]', chr):
            posting = utils.load_obj(os.path.join(self.outputPath, "postingDictTOI"))
        elif re.match(r'^[SWCswc]', chr):
            posting = utils.load_obj(os.path.join(self.outputPath, "postingDictSWC"))
        elif re.match(r'^[BPHbph]', chr):
            posting = utils.load_obj(os.path.join(self.outputPath, "postingDictBPH"))
        elif re.match(r'^[FMDfmd]', chr):
            posting = utils.load_obj(os.path.join(self.outputPath, "postingDictFMD"))
        elif re.match(r'^[RELrel]', chr):
            posting = utils.load_obj(os.path.join(self.outputPath, "postingDictREL"))
        elif re.match(r'^[NAGnag]', chr):
            posting = utils.load_obj(os.path.join(self.outputPath, "postingDictNAG"))
        elif re.match(r'^[UKVYukvy]', chr):
            posting = utils.load_obj(os.path.join(self.outputPath, "postingDictUKVY"))
        elif re.match(r'^[JQZXjqzx]', chr):
            posting = utils.load_obj(os.path.join(self.outputPath, "postingDictJQZX"))
        elif re.match(r'^[0-9]', chr):
            posting = utils.load_obj(os.path.join(self.outputPath, "postingDictNUM"))
        elif re.match(r'^#', chr):
            posting = utils.load_obj(os.path.join(self.outputPath, "postingDictHashtag"))
        elif re.match(r'^@', chr):
            posting = utils.load_obj(os.path.join(self.outputPath, "postingDictStrudel"))
        else:
            posting = utils.load_obj(os.path.join(self.outputPath, "postingDictSimbol"))
            # if term[1] in "Anthoni":
            #    print(term[1])

        for w in list_word:
            self.posting_doc[w] = posting[w.lower()]

    def exists_term_in_inverted(self,tokens):
        res = []
        for t in tokens:
            if t in self.inverted_index:
                res.append(t)
        return res

    def relevant_docs_from_posting(self, query,query_entities,model):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """
        # word2Vec
        #expend the query with similar words
        exp = self.expend_query_w2v(model,query)

        #load inverted index
        #inverted_index = utils.load_obj(os.path.join(self.outputPath,"inverted_idx"))
        #load document collection
        #document_collection = utils.load_obj(os.path.join(self.outputPath, "document_collection"))

        relevant_docs = {}
        #toLoadPostingAF =True
        #toLoadPostingGP = True
        #toLoadPostingQA = True
        #toLoadPostingSimbol = True

        #add the expended query to the term we looking for relevent doc
        if exp:
            full_tokens = query + exp
        else:
            full_tokens = query

        #do stemming on query terms
        if self.stemming:
            s = Stemmer()
            full_tokens = s.stem_term(full_tokens)
            query_entities = s.stem_term(query_entities)

    #handel the terms
        list_term = self.exists_term_in_inverted(full_tokens)

        #sort the tokens of the query
        dic_by_first_ch = splitLst(list_term)
        for k,v in dic_by_first_ch.items():
            self.load_posting(k,v)

        # handel the entities
        entities_posting = utils.load_obj(os.path.join(self.outputPath, "postingEntities"))
        entities_inv = utils.load_obj(os.path.join(self.outputPath, "inverted_idx_entities"))

        for e in query_entities:
            if e in entities_inv:
                self.posting_doc[e] = entities_posting[e.lower()]

        for t, v in self.posting_doc.items():
            # twiite id
            #print(v)
            for doc in v:
                #print(doc)
                doc_id = doc[0]
                # term ferqunce normal by max
                #print(doc[1],doc[3])
                doc_tf = doc[1] / doc[3]

                if doc_id not in relevant_docs.keys():
                    # doc terms
                    doc_uniqe_word = self.document_collection[doc_id].keys()
                    # doc vector
                    vec_doc = self.avg_vector(doc_uniqe_word, model)
                    # idf
                    idf_doc = math.log10(self.corpus_num_docs / self.inverted_index[t])
                    # numofDoc ,list of term match with the query, the wight (tf*idf),
                    relevant_docs[doc_id] = ReleventDocData(1, [(t, doc_tf * idf_doc)], doc[4], doc[5], vec_doc)

                else:
                    relevant_docs[doc_id].num_show += 1
                    relevant_docs[doc_id].terms.append((t, doc_tf * idf_doc))



        #for t in full_tokens:
            #try:
                #return how the term index in the posting
                #term = self.term_in_inve(t,self.inverted_index.keys())
                #if term[0]:
                    #if the term start with A-F load the relevent posting file , if its alredy loaded use him
        #            if re.match(r'^[A-Fa-f]', term[1]):
                        #if term[1] in "Anthoni":
                        #    print(term[1])
        #                if toLoadPostingAF:
        #                    postingAF = utils.load_obj(os.path.join(self.outputPath,"postingAF"))
        #                    toLoadPostingAF = False
                            #posting_doc = postingAF[term[1]]
        #                    self.posting_doc = postingAF[term[1].lower()]
        #                else:
                            #posting_doc = postingAF[term[1]]
        #                    self.posting_doc[term[1]] = postingAF[term[1].lower()]
                    # if the term start with G-P load the relevent posting file , if its alredy loded use him
        #            elif re.match(r'^[G-Pg-p]', term[1]):
        #                if toLoadPostingGP:
        #                    postingGP = utils.load_obj(os.path.join(self.outputPath,"postingGP"))
        #                    toLoadPostingGP = False
                            #posting_doc = postingGP[term[1]]
        #                    self.posting_doc[term[1]] = postingGP[term[1].lower()]
        #                else:
                            #posting_doc = postingGP[term[1]]
        #                    self.posting_doc[term[1]] = postingGP[term[1].lower()]
                    # if the term start with Q-Z load the relevent posting file , if its alredy loded use him
        #            elif re.match(r'^[Q-Zq-z]', term[1]):
        #                if toLoadPostingQA:
        #                    postingQA = utils.load_obj(os.path.join(self.outputPath,"postingQZ"))
        #                    toLoadPostingQA = False
                            #posting_doc = postingQA[term[1]]
        #                    self.posting_doc[term[1]] = postingQA[term[1].lower()]
        #                else:
                            #posting_doc = postingQA[term[1]]
        #                    self.posting_doc[term[1]] = postingQA[term[1].lower()]
        #            else:
                        # if the term start with Simbol load the relevent posting file , if its alredy loded use him
        #                if toLoadPostingSimbol:
        #                    postingSimbol = utils.load_obj(os.path.join(self.outputPath,"postingSimbol"))
        #                    toLoadPostingSimbol = False
                            #posting_doc = postingSimbol[term[1]]
        #                    self.posting_doc[term[1]] = postingSimbol[term[1].lower()]
        #                else:
                            #posting_doc = postingSimbol[term[1]]
        #                    self.posting_doc[term[1]] = postingSimbol[term[1].lower()]


        #        for k,v in self.posting_doc.items():
                    #twiite id
        #            doc = v
        #            doc_id = doc[0]
                        # term ferqunce normal by max
        #            doc_tf = doc[1] / doc[3]

         #           if doc_id not in relevant_docs.keys():
                            # doc terms
         #               doc_uniqe_word = self.document_collection[doc_id].keys()
                            # doc vector
         #               vec_doc = self.avg_vector(doc_uniqe_word, model)
                            # idf
         #               idf_doc = math.log10(self.corpus_num_docs / self.inverted_index[term[1]])
                            # numofDoc ,list of term match with the query, the wight (tf*idf),
         #               relevant_docs[doc_id] = ReleventDocData(1,[(t,doc_tf*idf_doc)],doc[4],doc[5],vec_doc)

         #           else:
         #               relevant_docs[doc_id].num_show += 1
         #               relevant_docs[doc_id].terms.append((t,doc_tf*idf_doc))

            #except:
            #    print('term {} not found in posting'.format(t))

        return relevant_docs
        # ,self.freq_terms_query(full_tokens)
