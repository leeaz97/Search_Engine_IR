from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
from stemmer import Stemmer
import utils
import os

def mearge_posting(indexer):
    postingAF = utils.load_obj("postingAF")
    postingGP = utils.load_obj("postingGP")
    postingQZ = utils.load_obj("postingQZ")
    postingSimbol = utils.load_obj("postingSimbol")

    for k,v in indexer.postingDictAF.items():
        if k in postingAF.keys():
            for i in v:
                postingAF[k].append(i)
        else:
            postingAF[k] = v

    for k,v in indexer.postingDictGP.items():
        if k in postingGP.keys():
            for i in v:
                postingGP[k].append(i)
        else:
            postingGP[k] = v

    for k,v in indexer.postingDictQZ.items():
        if k in postingQZ.keys():
            for i in v:
                postingQZ[k].append(i)
        else:
            postingQZ[k] = v

    for k,v in indexer.postingDictSimbol.items():
        if k in postingSimbol.keys():
            for i in v:
                postingSimbol[k].append(i)
        else:
            postingSimbol[k] = v

    utils.save_obj(postingAF, "postingAF")
    utils.save_obj(postingGP, "postingGP")
    utils.save_obj(postingQZ, "postingQZ")
    utils.save_obj(postingSimbol, "postingSimbol")

#    return

def run_engine(config):
    """
    :return:
    """
    number_of_documents = 0
    num_doc_topost = 0
    to_mearge = False

    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse(config)
    indexer = Indexer(config)

    #indexer_without_stremming = Indexer(config)

    #f = open("demofile2.txt", "a")
    #over all files in the dir of the corpus
    for subdir, dirs, files in os.walk(config.get__corpusPath()):
        for file in files:
            filepath = subdir + os.sep + file

            if file.endswith(".parquet"):
                documents_list = r.read_file(file_name=filepath)
                # Iterate over every document in the file
                for idx, document in enumerate(documents_list):
                    # parse the document
                    parsed_document = p.parse_doc(document)
                    #print(parsed_document.term_doc_dictionary,parsed_document_stremming.term_doc_dictionary)
                    number_of_documents += 1
                    # index the document data
                    indexer.add_new_doc(parsed_document)

                    if num_doc_topost <= 1000:
                        num_doc_topost += 1
                        print(num_doc_topost)
                    else:
                        if to_mearge:
                            print("to mearge")
                            mearge_posting(indexer)

                            indexer.init_posting()
                            to_mearge = False
                        else:
                            utils.save_obj(indexer.postingDictAF, "postingAF")
                            utils.save_obj(indexer.postingDictGP, "postingGP")
                            utils.save_obj(indexer.postingDictQZ, "postingQZ")
                            utils.save_obj(indexer.postingDictSimbol, "postingSimbol")
                            indexer.init_posting()
                            to_mearge = True
                        num_doc_topost = 0
                        #posting_num+=1

                    if number_of_documents == 3000:
                        break
            if number_of_documents == 3000:
                break
        if number_of_documents == 3000:
            break


    utils.save_obj(indexer.inverted_idx, "inverted_idx")
    print('Finished parsing and indexing. Starting to export files')

#    utils.save_obj(indexer_without_stremming.inverted_idx, "inverted_idx_without_stremming")
#    utils.save_obj(indexer_without_stremming.postingDict, "posting_without_stremming")
    #utils.save_obj(indexer.inverted_idx, "inverted_idx")
    #utils.save_obj(indexer.postingDict, "posting")
    return number_of_documents

def load_index(name_index):
    print('Load inverted index')
    inverted_index = utils.load_obj(name_index)
    return inverted_index


def search_and_rank_query(query,inverted_index,k,config):
    p = Parse(config)
    #query_as_list = p.parse_sentence(query)
    query_as_list = p.parse_sentence(query)[0]

    #if config.toStem:
    #    s = Stemmer()
    #    query_as_list = s.stem_term(query_as_list)

    searcher = Searcher(inverted_index,config)
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    return searcher.ranker.retrieve_top_k(ranked_docs, k)


def main(corpus_path=r"C:\Users\lazrati\Desktop\leeStudy\Data\Data\date=07-09-2020",output_path=r"C:\Users\lazrati\Desktop\leeStudy\Data",stemming=True,queries=[],num_doc_to_retrive=2000):

    config = ConfigClass()
    config.corpusPath = corpus_path
    config.savedFileMainFolder = output_path
    config.toStem = stemming

    number_of_documents = run_engine(config)
    config.number_of_documents = number_of_documents

    #query = input("Please enter a query: ")
    queries = ["Dr. Anthony Fauci wrote in a 2005 paper published in Virology Journal that hydroxychloroquine was effective in treating SARS.",
              "The seasonal flu kills more people every year in the U.S. than COVID-19 has to date.","Coronavirus is less dangerous than the flu",
              "Microsoft co-founder Bill Gates said \"only the people who have all the vaccines will still be able to move freely\"."]
    #k = int(input("Please enter number of docs to retrieve: "))

    # limit the doc retrive to 2000
    if num_doc_to_retrive>2000:
        num_doc_to_retrive=2000

    #load the relevant index
    #if stemming:
    #    inverted_index = load_index("inverted_idx_stremming")
    #else:
    #    inverted_index = load_index("inverted_idx_without_stremming")
    inverted_index = load_index("inverted_idx")

    if queries:
        if isinstance(queries, list):
            for query in queries:
                for doc_tuple in search_and_rank_query(query, inverted_index, num_doc_to_retrive,config):
                    print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
        else:
            file = open(queries, 'r')
            queries = file.readlines()
            for q in queries:
                for doc_tuple in search_and_rank_query(q, inverted_index, num_doc_to_retrive,config):
                    print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))



