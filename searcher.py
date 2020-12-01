from parser_module import Parse
from ranker import Ranker
from ReleventDoc import ReleventDocData
import utils
import re

class Searcher:

    def __init__(self, inverted_index,config):#,stemming):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse(config)
        self.ranker = Ranker()
        self.inverted_index = inverted_index
        #self.stemming = stemming

    #normal the query?
    def freq_terms_query(self,list_query):
        term_dict = {}
        for term in list_query:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1
        return term_dict

    def relevant_docs_from_posting(self, query):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """

        #posting = utils.load_obj("posting")
        inverted_index = utils.load_obj("inverted_idx")

        toLoadPostingAF =True
        toLoadPostingGP = True
        toLoadPostingQA = True
        toLoadPostingSimbol = True

        #word2Vec

        #need to check how the term save in the courps (lower apper ...)
        relevant_docs = {}
        #relevant_doc = ReleventDocData()
        #len_terms_query = len(query)

        for term in query:
            try:
                if re.match(r'^[A-Fa-f]', term):
                    if toLoadPostingAF:
                        postingAF = utils.load_obj("postingAF")
                        toLoadPostingAF = False
                        posting_doc = postingAF[term]
                    else:
                        posting_doc = postingAF[term]
                elif re.match(r'^[G-Pg-p]', term):
                    if toLoadPostingGP:
                        postingGP = utils.load_obj("postingGP")
                        toLoadPostingGP = False
                        posting_doc = postingGP[term]
                    else:
                        posting_doc = postingGP[term]
                elif re.match(r'^[Q-Zq-z]', term):
                    if toLoadPostingQA:
                        postingQA = utils.load_obj("postingQZ")
                        toLoadPostingQA = False
                        posting_doc = postingQA[term]
                    else:
                        posting_doc = postingQA[term]
                else: #Simbol
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
                    doc_time = docs[5]

                    if doc_id not in relevant_docs.keys():
                        relevant_docs[doc_id] = ReleventDocData(1,[(term,idf_doc,doc_tf,doc_time)])
                            #relevant_docs[doc_id].num_id += relevant_doc.num_id
                            #relevant_docs[doc_id] = (1,[(term,doc_tf,df_doc,doc_time)])
                    else:
                        relevant_docs[doc_id].num_id += 1
                        relevant_docs[doc_id].terms.append((term,idf_doc,doc_tf,doc_time))
                        #relevant_docs[doc_id][1].append((term,doc_tf,df_doc,doc_time))
            except:
                print('term {} not found in posting'.format(term))
        #print(relevant_docs)
        return relevant_docs
