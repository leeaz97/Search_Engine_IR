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

class Searcher:

    def __init__(self, inverted_index,config):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse(config)
        self.ranker = Ranker()
        self.inverted_index = inverted_index
        self.stemming = config.toStem
        self.outputPath = config.get__outputPath()
        self.num_doc = config.number_of_documents

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

    def term_in_inve(self,term,k):
        if term in k:
            return (True,term)
        if term.lower() in k:
            return (True,term.lower())
        if term.upper() in k:
            return (True,term.upper())
        if term[0].lower()+term[1:] in k:
            return (True,term[0].lower()+term[1:])
        if term[0].upper()+term[1:] in k:
            return (True,term[0].upper()+term[1:])
        return (False, '')

    def relevant_docs_from_posting(self, query,model):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """
        # word2Vec
        #expend the query with similar words
        exp = self.expend_query_w2v(model,query)

        #load inverted index
        inverted_index = utils.load_obj(os.path.join(self.outputPath,"inverted_idx"))

        relevant_docs = {}
        toLoadPostingAF =True
        toLoadPostingGP = True
        toLoadPostingQA = True
        toLoadPostingSimbol = True

        #add the expended query to the term we looking for relevent doc
        if exp:
            full_tokens = query + exp
        else:
            full_tokens = query

        #do stemming on query terms
        if self.stemming:
            s = Stemmer()
            full_tokens = s.stem_term(full_tokens)

        for t in full_tokens:
            #try:
                #return how the term index in the posting
                term = self.term_in_inve(t,inverted_index.keys())
                if term[0]:
                    #if the term start with A-F load the relevent posting file , if its alredy loaded use him
                    if re.match(r'^[A-Fa-f]', term[1]):
                        #if term[1] in "Anthoni":
                        #    print(term[1])
                        if toLoadPostingAF:
                            postingAF = utils.load_obj(os.path.join(self.outputPath,"postingAF"))
                            toLoadPostingAF = False
                            posting_doc = postingAF[term[1]]
                        else:
                            posting_doc = postingAF[term[1]]
                    # if the term start with G-P load the relevent posting file , if its alredy loded use him
                    elif re.match(r'^[G-Pg-p]', term[1]):
                        if toLoadPostingGP:
                            postingGP = utils.load_obj(os.path.join(self.outputPath,"postingGP"))
                            toLoadPostingGP = False
                            posting_doc = postingGP[term[1]]
                        else:
                            posting_doc = postingGP[term[1]]
                    # if the term start with Q-Z load the relevent posting file , if its alredy loded use him
                    elif re.match(r'^[Q-Zq-z]', term[1]):
                        if toLoadPostingQA:
                            postingQA = utils.load_obj(os.path.join(self.outputPath,"postingQZ"))
                            toLoadPostingQA = False
                            posting_doc = postingQA[term[1]]
                        else:
                            posting_doc = postingQA[term[1]]
                    else:
                        # if the term start with Simbol load the relevent posting file , if its alredy loded use him
                        if toLoadPostingSimbol:
                            postingSimbol = utils.load_obj(os.path.join(self.outputPath,"postingSimbol"))
                            toLoadPostingSimbol = False
                            posting_doc = postingSimbol[term[1]]
                        else:
                            posting_doc = postingSimbol[term[1]]



                    for docs in posting_doc:
                        #twiite id
                        doc_id = docs[0]
                        # term ferqunce
                        doc_tf = docs[3]
                        #normal doc freq -docs[5]
                        #date - docs[6]

                        if doc_id not in relevant_docs.keys():
                            # doc vector
                            vec_doc = self.avg_vector(docs[7], model)
                            # idf
                            idf_doc = math.log10(self.num_doc / inverted_index[term[1]])

                            relevant_docs[doc_id] = ReleventDocData(1,[(t,doc_tf)],idf_doc,docs[6],docs[5],vec_doc)
                                #relevant_docs[doc_id].num_id += relevant_doc.num_id
                                #relevant_docs[doc_id] = (1,[(term,doc_tf,df_doc,doc_time)])
                        else:
                            relevant_docs[doc_id].num_id += 1
                            relevant_docs[doc_id].terms.append((t,doc_tf))
                            #relevant_docs[doc_id].nf = doc_nf
                            #relevant_docs[doc_id].vec_doc = vec_doc
                            #,idf_doc
                            #doc_time

            #except:
            #    print('term {} not found in posting'.format(t))

        return relevant_docs # ,self.freq_terms_query(full_tokens)
