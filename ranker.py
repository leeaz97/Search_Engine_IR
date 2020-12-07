import math
from numpy import dot
from numpy.linalg import norm
import numpy as np

def con_sin(vec_doc, vec_query):
    if not np.all((norm(vec_doc) * norm(vec_query))==0):
        cos_sim = dot(vec_doc, vec_query) / (norm(vec_doc) * norm(vec_query))
        return cos_sim
    else:
        return 0

class Ranker:
    def __init__(self):
        pass

    @staticmethod
    def rank_relevant_doc(relevant_doc,query_dict,query_vec):
        """
        This function provides rank for each relevant document and sorts them by their scores.
        The current score considers solely the number of terms shared by the tweet (full_text) and query.
        :param relevant_doc: dictionary of documents that contains at least one term from the query.
        :return: sorted list of documents by score
        """
        ranking_doc = {}
        nf_query = 1/math.sqrt(sum(pow(item,2) for item in query_dict.values()))

        for k,v in relevant_doc.items():
            for i in v.terms:
                if i[0] in query_dict.keys():
                    rank = ( (0.4 * ((i[1] * query_dict[i[0]]) * (v.nf * nf_query))) + ((1 - 0.4) * con_sin(v.vec_doc, query_vec)))*v.num_show
                    ranking_doc[k] = rank

        return sorted(ranking_doc.items(), key=lambda item: item[1], reverse=True)

    @staticmethod
    def retrieve_top_k(sorted_relevant_doc, k=1):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """
        return sorted_relevant_doc[:k]
