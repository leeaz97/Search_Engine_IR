from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
from stemmer import Stemmer
import utils
import os
from datetime import datetime
import csv


def sorted_dic_by_listval(unsorted_dict):
    return dict(sorted(unsorted_dict.items()))

def mearge_posting(indexer):
    postingAF = utils.load_obj("postingAF")
    postingGP = utils.load_obj("postingGP")
    postingQZ = utils.load_obj("postingQZ")
    postingSimbol = utils.load_obj("postingSimbol")

    try:
        for k,v in indexer.postingDictAF.items():
            if k in postingAF.keys():
                for i in v:
                    postingAF[k].append(i)
            elif k[0].isupper() and k.lower() in postingAF.keys():
                for i in v:
                    postingAF[k.lower()].append(i)
            elif k[0].isupper() and k[0].lower()+k[1:] in postingAF.keys():
                for i in v:
                    postingAF[k[0].lower()+k[1:]].append(i)
            elif k[0].islower() and k[0].upper()+k[1:] in postingAF.keys():
                temp = postingAF.pop(k[0].upper() + k[1:])
                postingAF[k] = []
                for i in temp:
                    postingAF[k].append(i)
                for i in v:
                    postingAF[k].append(i)
            else:
                postingAF[k] = v

        for k,v in indexer.postingDictGP.items():
            if k in postingGP.keys():
                for i in v:
                    postingGP[k].append(i)
            elif k[0].isupper() and k.lower() in postingGP.keys():
                for i in v:
                    postingGP[k.lower()].append(i)
            elif k[0].isupper() and k[0].lower() + k[1:] in postingGP.keys():
                for i in v:
                    postingGP[k[0].lower() + k[1:]].append(i)
            elif k[0].islower() and k[0].upper() + k[1:] in postingGP.keys():
                temp = postingGP.pop(k[0].upper() + k[1:])
                postingGP[k] = []
                for i in temp:
                    postingGP[k].append(i)
                for i in v:
                    postingGP[k].append(i)
            else:
                postingGP[k] = v

        for k,v in indexer.postingDictQZ.items():
            if k in postingQZ.keys():
                for i in v:
                    postingQZ[k].append(i)
            elif k[0].isupper() and k.lower() in postingQZ.keys():
                for i in v:
                    postingQZ[k.lower()].append(i)
            elif k[0].isupper() and k[0].lower() + k[1:] in postingQZ.keys():
                for i in v:
                    postingQZ[k[0].lower() + k[1:]].append(i)
            elif k[0].islower() and k[0].upper() + k[1:] in postingQZ.keys():
                temp = postingQZ.pop(k[0].upper() + k[1:])
                postingQZ[k] = []
                for i in temp:
                    postingQZ[k].append(i)
                for i in v:
                    postingQZ[k].append(i)
            else:
                postingQZ[k] = v

        for k,v in indexer.postingDictSimbol.items():
            if k in postingSimbol.keys():
                for i in v:
                    postingSimbol[k].append(i)
            elif k[0].isupper() and k.lower() in postingSimbol.keys():
                for i in v:
                    postingSimbol[k.lower()].append(i)
            elif k[0].isupper() and k[0].lower() + k[1:] in postingSimbol.keys():
                for i in v:
                    postingSimbol[k[0].lower() + k[1:]].append(i)
            elif k[0].islower() and k[0].upper() + k[1:] in postingSimbol.keys():
                temp = postingSimbol.pop(k[0].upper() + k[1:])
                postingSimbol[k] = []
                for i in temp:
                    postingSimbol[k].append(i)
                for i in v:
                    postingSimbol[k].append(i)
            else:
                postingSimbol[k] = v

    except:
        print('problem in mearg with the following key {}'.format(k))

    #sorting the posting file
    postingAF = sorted_dic_by_listval(postingAF)
    postingGP = sorted_dic_by_listval(postingGP)
    postingQZ = sorted_dic_by_listval(postingQZ)
    postingSimbol = sorted_dic_by_listval(postingSimbol)

    #save the mearge file in the disk
    utils.save_obj(postingAF, "postingAF")
    utils.save_obj(postingGP, "postingGP")
    utils.save_obj(postingQZ, "postingQZ")
    utils.save_obj(postingSimbol, "postingSimbol")


#def avg_veactor_toDoc(w2v_model, tokens):
#    vectors = np.array([])
#    first_element = True
    #gensim.models.Word2Vec.wv.vocab
#    if tokens:
#        for word in tokens:
#            if word in w2v_model.vocab:
#                if first_element:
#                    vectors = np.array(w2v_model.wv.get_vector(word, norm=True))
#                    first_element = False
                #print(w2v_model.wv[word])
#                else :
#                    np.concatenate((vectors, w2v_model.wv.get_vector(word, norm=True)))
                #vectors = w2v_model.wv[word]
                #print(type(w2v_model.vocab))
                #vector = word_vectors.wv.get_vector('office', norm=True)

            #vectors = model.wv[t]
#        if vectors:
#            print(np.average(vectors))
#            print("-----------------------------------")
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
                    if parsed_document == None:
                        continue
                    #print(parsed_document.term_doc_dictionary,parsed_document_stremming.term_doc_dictionary)
                    number_of_documents += 1
                    # index the document data
                    indexer.add_new_doc(parsed_document)
                    #avg_veactor_toDoc(model,parsed_document.term_doc_dictionary.keys())

                    if num_doc_topost <= 100:
                        num_doc_topost += 1
                        #print(num_doc_topost)
                    else:
                        if to_mearge:
                            #print("to mearge")
                            mearge_posting(indexer)
                            indexer.init_posting()
                            to_mearge = True
                        else:
                            utils.save_obj(indexer.postingDictAF, "postingAF")
                            utils.save_obj(indexer.postingDictGP, "postingGP")
                            utils.save_obj(indexer.postingDictQZ, "postingQZ")
                            utils.save_obj(indexer.postingDictSimbol, "postingSimbol")
                            indexer.init_posting()
                            to_mearge = True
                        num_doc_topost = 0
                        #posting_num+=1
                    #print("num of doc", number_of_documents)

                    if number_of_documents == 1000:
                        break
            if number_of_documents == 1000:
                break
        if number_of_documents == 1000:
            break

    indexer.add_idf(number_of_documents)
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
    relevant_docs , query_tf = searcher.relevant_docs_from_posting(query_as_list)
    #query_tf = searcher.freq_terms_query(query_as_list)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs,query_tf)
    print(ranked_docs)
    return searcher.ranker.retrieve_top_k(ranked_docs, k)


def main(corpus_path=r"C:\Users\lazrati\Desktop\leeStudy\Data\Data",output_path=r"C:\Users\lazrati\Desktop\leeStudy\Data",stemming=True,queries=[],num_doc_to_retrive=2000):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    config = ConfigClass()
    config.corpusPath = corpus_path
    config.savedFileMainFolder = output_path
    config.toStem = stemming

    number_of_documents = run_engine(config)
    config.number_of_documents = number_of_documents

    now_after_all = datetime.now()
    print("Diff Time =", now_after_all-now)

    #query = input("Please enter a query: ")
    queries = ["Dr. Anthony Fauci wrote in a 2005 paper published in Virology Journal that hydroxychloroquine was effective in treating SARS.",
              "The seasonal flu kills more people every year in the U.S. than COVID-19 has to date.","Coronavirus is less dangerous than the flu",
              "Microsoft co-founder Bill Gates said \"only the people who have all the vaccines will still be able to move freely\"."]
    #k = int(input("Please enter number of docs to retrieve: "))

    # limit the doc retrive to 2000
    if num_doc_to_retrive>2000:
        num_doc_to_retrive=2000


    inverted_index = load_index("inverted_idx")

    if queries:
        with open('result.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['query_id', 'tweet id', 'score'])
            if isinstance(queries, list):
                for query in range(len(queries)):
                    for doc_tuple in search_and_rank_query(queries[query], inverted_index, num_doc_to_retrive,config):
                        print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
                        writer.writerow([query, doc_tuple[0], doc_tuple[1]])

            else:
                file = open(queries, 'r')
                queries = file.readlines()
                for query in range(list(queries)):
                    for doc_tuple in search_and_rank_query(queries[query], inverted_index, num_doc_to_retrive,config):
                        print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
                        writer.writerow([query, doc_tuple[0], doc_tuple[1]])

    now_after_all = datetime.now()
    print("Diff Time =", now_after_all-now)




