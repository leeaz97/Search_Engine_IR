from parser_module import Parse
from ranker import Ranker
from ReleventDoc import ReleventDocData
import utils
import re
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

    #normal the query?
    def freq_terms_query(self,list_query):
        term_dict = {}
        for term in list_query:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1
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
                #result = word_vectors.similar_by_word("cat")
                #most_similar_key, similarity = result[0]  # look at the first match
                #print(f"{most_similar_key}: {similarity:.4f}")

    def relevant_docs_from_posting(self, query):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """
        # word2Vec
        #load the model
        model = utils.load_GoogleNews_vectors_negative300('GoogleNews-vectors-negative300.bin')
        #print(type(model))
        #expend the query with similar words
        exp = self.expend_query_w2v(model,query)

        #posting = utils.load_obj("posting")
        inverted_index = utils.load_obj("inverted_idx")

        toLoadPostingAF =True
        toLoadPostingGP = True
        toLoadPostingQA = True
        toLoadPostingSimbol = True

        if exp:
            full_tokens = query + exp
        else:
            full_tokens = query

        if self.stemming:
            s = Stemmer()
            full_tokens = s.stem_term(full_tokens)

        #need to check how the term save in the courps (lower apper ...)
        relevant_docs = {}
        #relevant_doc = ReleventDocData()
        #len_terms_query = len(query)

        for term in full_tokens:
            try:
                if term in inverted_index.keys():
                    #if the term start with A-F load the relevent posting file , if its alredy loded use him
                    if re.match(r'^[A-Fa-f]', term):
                        if toLoadPostingAF:
                            postingAF = utils.load_obj("postingAF")
                            toLoadPostingAF = False
                            posting_doc = postingAF[term]
                        else:
                            posting_doc = postingAF[term]
                    # if the term start with G-P load the relevent posting file , if its alredy loded use him
                    elif re.match(r'^[G-Pg-p]', term):
                        if toLoadPostingGP:
                            postingGP = utils.load_obj("postingGP")
                            toLoadPostingGP = False
                            posting_doc = postingGP[term]
                        else:
                            posting_doc = postingGP[term]
                    # if the term start with Q-Z load the relevent posting file , if its alredy loded use him
                    elif re.match(r'^[Q-Zq-z]', term):
                        if toLoadPostingQA:
                            postingQA = utils.load_obj("postingQZ")
                            toLoadPostingQA = False
                            posting_doc = postingQA[term]
                        else:
                            posting_doc = postingQA[term]
                    else:
                        # if the term start with Simbol load the relevent posting file , if its alredy loded use him
                        if toLoadPostingSimbol:
                            postingSimbol = utils.load_obj("postingSimbol")
                            toLoadPostingSimbol = False
                            posting_doc = postingSimbol[term]
                        else:
                            posting_doc = postingSimbol[term]

                        #idf
                    idf_doc = inverted_index[term][1]
                        #print("posting to term in query {}",term,posting_doc)
                    for docs in posting_doc:
                        doc_id = docs[0]
                        # term ferqunce
                        doc_tf = docs[3]
                        #normal doc freq
                        doc_nf = docs[5]
                        doc_time = docs[6]

                        if doc_id not in relevant_docs.keys():
                            relevant_docs[doc_id] = ReleventDocData(1,[(term,idf_doc,doc_tf,doc_nf,doc_time)])
                                #relevant_docs[doc_id].num_id += relevant_doc.num_id
                                #relevant_docs[doc_id] = (1,[(term,doc_tf,df_doc,doc_time)])
                        else:
                            relevant_docs[doc_id].num_id += 1
                            relevant_docs[doc_id].terms.append((term,idf_doc,doc_tf,doc_nf,doc_time))
                            #relevant_docs[doc_id][1].append((term,doc_tf,df_doc,doc_time))
            except:
                print('term {} not found in posting'.format(term))
        #print(relevant_docs)
        return relevant_docs ,self.freq_terms_query(full_tokens)
