from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils
import os


def run_engine(corpus_path,output_path,stemming):
    """
    :return:
    """
    number_of_documents = 0

    config = ConfigClass()
    config.corpusPath = corpus_path
    config.savedFileMainFolder = output_path
    config.toStem = stemming

    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse()
    indexer_stremming = Indexer(config)
    indexer_without_stremming = Indexer(config)

    f = open("demofile2.txt", "a")
    for subdir, dirs, files in os.walk(config.get__corpusPath()):
        for file in files:
            filepath = subdir + os.sep + file

            if file.endswith(".parquet"):
                documents_list = r.read_file(file_name=filepath)
                # Iterate over every document in the file
                for idx, document in enumerate(documents_list):
                    # parse the document
                    parsed_document,parsed_document_stremming = p.parse_doc(document)
                    #print(parsed_document.term_doc_dictionary,parsed_document_stremming.term_doc_dictionary)
                    number_of_documents += 1
                    # index the document data
                    indexer_without_stremming.add_new_doc(parsed_document)
                    indexer_stremming.add_new_doc(parsed_document_stremming)

                    if number_of_documents == 200:
                        break
            if number_of_documents == 200:
                break
        if number_of_documents == 200:
            break
    print('Finished parsing and indexing. Starting to export files')

    utils.save_obj(indexer_without_stremming.inverted_idx, "inverted_idx_without_stremming")
    utils.save_obj(indexer_without_stremming.postingDict, "posting_without_stremming")
    utils.save_obj(indexer_stremming.inverted_idx, "inverted_idx_stremming")
    utils.save_obj(indexer_stremming.postingDict, "posting_stremming")


def load_index(name_index):
    print('Load inverted index')
    inverted_index = utils.load_obj(name_index)
    return inverted_index


def search_and_rank_query(query, inverted_index, k):
    p = Parse()
    query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index)
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    return searcher.ranker.retrieve_top_k(ranked_docs, k)


def main(corpus_path=r"C:\Users\lazrati\Desktop\leeStudy\Data\Data\date=07-09-2020",output_path=r"C:\Users\lazrati\Desktop\leeStudy\Data",stemming=False,queris=[],num_doc_to_retrive=100):
    run_engine(corpus_path,output_path,stemming)
    #query = input("Please enter a query: ")
    #k = int(input("Please enter number of docs to retrieve: "))
    if stemming:
        inverted_index = load_index("inverted_idx_stremming")
    else:
        inverted_index = load_index("inverted_idx_without_stremming")
    if queris:
        if isinstance(queris, list):
            for query in queris:
                for doc_tuple in search_and_rank_query(query, inverted_index, num_doc_to_retrive):
                    print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
        else:
            file = open(queris, 'r')
            queries = file.readlines()
            for q in queries:
                for doc_tuple in search_and_rank_query(q, inverted_index, num_doc_to_retrive):
                    print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))



