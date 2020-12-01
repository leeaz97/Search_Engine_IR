class Ranker:
    def __init__(self):
        pass

    @staticmethod
    def rank_relevant_doc(relevant_doc,query_dict):
        """
        This function provides rank for each relevant document and sorts them by their scores.
        The current score considers solely the number of terms shared by the tweet (full_text) and query.
        :param relevant_doc: dictionary of documents that contains at least one term from the query.
        :return: sorted list of documents by score
        """
        #(idf_doc, doc_tf, doc_time)
        ranking_doc = {}
        #print(relevant_doc)
        for k,v in relevant_doc.items():
            for i in v.terms:
                if k not in ranking_doc.keys():
                    ranking_doc[k] = i[1] * i[2] * query_dict[i[0]]
                else:
                    ranking_doc[k] += i[1] * i[2] * query_dict[i[0]]

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
