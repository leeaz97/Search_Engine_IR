from parser_module import Parse
from ranker import Ranker
import utils


class Searcher:

    def __init__(self, inverted_index,config):#,stemming):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse(config)
        self.ranker = Ranker()
        self.inverted_index = inverted_index
        #self.stemming = stemming

    def relevant_docs_from_posting(self, query):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """
        #if self.stemming:
        #    posting = utils.load_obj("posting_stremming")
        #else:
        #    posting = utils.load_obj("posting_without_stremming")

        posting = utils.load_obj("posting")
        inverted_index = utils.load_obj("inverted_idx")

        #word2Vec
        relevant_docs = {}
        for term in query:
            try:
                posting_doc = posting[term]
                #amount of time term show in courpus - doc ferqunce
                df_doc = inverted_index[term]
                print("posting to term in query {}",term,posting_doc)
                for docs in posting_doc:
                    doc_id = docs[0]
                    # term ferqunce
                    doc_tf = docs[3]
                    doc_time = docs[5]

                    if doc_id not in relevant_docs.keys():
                        relevant_docs[doc_id] = 1
                        #relevant_docs[doc_id] = (1,[(term,doc_tf,df_doc,doc_time)])
                    else:
                        relevant_docs[doc_id] += 1
                        #relevant_docs[doc_id][1].append((term,doc_tf,df_doc,doc_time))
            except:
                print('term {} not found in posting'.format(term))
        print(relevant_docs)
        return relevant_docs
