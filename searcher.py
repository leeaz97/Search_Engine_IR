from parser_module import Parse
from ranker import Ranker
import utils


class Searcher:

    def __init__(self, inverted_index,stemming):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse()
        self.ranker = Ranker()
        self.inverted_index = inverted_index
        self.stemming = stemming

    def relevant_docs_from_posting(self, query):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """
        if self.stemming:
            posting = utils.load_obj("posting_stremming")
        else:
            posting = utils.load_obj("posting_without_stremming")

        relevant_docs = {}
        for term in query:
            try: # an example of checks that you have to do
                posting_doc = posting[term]
                print("posting to term in query {}",term,posting_doc)
                for docs in posting_doc:
                    doc_id = docs[0]
                    if doc_id not in relevant_docs.keys():
                        relevant_docs[doc_id] = 1
                    else:
                        relevant_docs[doc_id] += 1
            except:
                print('term {} not found in posting'.format(term))
        return relevant_docs
