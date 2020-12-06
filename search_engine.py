from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
from stemmer import Stemmer
import numpy as np
import utils
import os
from datetime import datetime
import csv


def sorted_dic_by_key(unsorted_dict):
    return dict(sorted(unsorted_dict.items()))

def sorted_dic_by_val(unsorted_dict):#,term,post_file):
    # sort the posting by tweet_id
    for term in unsorted_dict.keys():
        sorted(unsorted_dict[term], key=lambda x: x[0])
    return unsorted_dict

'''def mearge_2dic(dic1,dic2):
    for k, v in dic1.items():
        if k in dic2.keys():
            #for i in v:
            dic2[k]+v#.append(i)
        elif k[0].isupper() and k.lower() in dic2.keys():
            for i in v:
                dic2[k.lower()]+v#.append(i)
        elif k[0].isupper() and k[0].lower() + k[1:] in dic2.keys():
            for i in v:
                dic2[k[0].lower() + k[1:]]+v#.append(i)
        elif k[0].islower() and k[0].upper() + k[1:] in dic2.keys():
            temp = dic2.pop(k[0].upper() + k[1:])
            dic2[k] = temp+v
            #for i in temp:
            #    dic2[k].append(i)
            #for i in v:
            #     dic2[k].append(i)
        else:
            dic2[k] = v

    # sorting the posting file
    return sorted_dic_by_val(dic2)'''

def new_merge_2dic(dic1,dic2):
    for k,v in dic2.items():
        if k in dic1.keys():
            dic1[k] += v
        else:
            dic1[k] = v
    #z = {**dic1, **dic2}
    return dic1

def merge_posting(path,pos_num):
    #load the first posting file
    posting = utils.load_obj(path+'_1')
    for i in range(2,pos_num+1):
        posting = new_merge_2dic(posting,utils.load_obj(path+'_'+str(i)))

    posting_merge1 = sorted_dic_by_val(posting)
    posting_merge2 = sorted_dic_by_key(posting_merge1)
    utils.save_obj(posting_merge2, path)

def merge_doc_collection(path,pos_num):
    posting = utils.load_obj(path + '_1')
    for i in range(2, pos_num + 1):
        posting = new_merge_2dic(posting, utils.load_obj(path + '_' + str(i)))

    utils.save_obj(posting, path)

def main_merge(stem_outPath,posting_num):
    merge_posting(os.path.join(stem_outPath, "postingAF"),posting_num)
    merge_posting(os.path.join(stem_outPath, "postingGP"),posting_num)
    merge_posting(os.path.join(stem_outPath, "postingQZ"),posting_num)
    merge_posting(os.path.join(stem_outPath, "postingSimbol"),posting_num)

    merge_doc_collection(os.path.join(stem_outPath, "document_collection"),posting_num)


def save_posting_and_doc_collection(indexer,path,posting_num):
    utils.save_obj(indexer.document_collection, os.path.join(path, "document_collection_" + str(posting_num)))
    utils.save_obj(indexer.postingDictAF, os.path.join(path, "postingAF_" + str(posting_num)))
    utils.save_obj(indexer.postingDictGP, os.path.join(path, "postingGP_" + str(posting_num)))
    utils.save_obj(indexer.postingDictQZ, os.path.join(path, "postingQZ_" + str(posting_num)))
    utils.save_obj(indexer.postingDictSimbol, os.path.join(path, "postingSimbol_" + str(posting_num)))


def run_engine(config):
    """
    :return:
    """
    number_of_documents = 0
    num_doc_topost = 0
    posting_num = 1
    #to_mearge = False

    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse(config)
    indexer = Indexer(config)
    stem_outPath = config.get__outputPath()


    if not os.path.exists(stem_outPath):
        os.makedirs(stem_outPath)

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

                    # continue is return empty document
                    if parsed_document == None:
                        continue

                    #count the num of
                    number_of_documents += 1

                    # index the doc
                    indexer.add_new_doc(parsed_document)

                    # index to posting the document data
                    if num_doc_topost < 200000:
                        num_doc_topost += 1
                    else:
                        #indexer.sorted_posting()
                        # index the document_collection
                        # ? indexer.sorted_posting()
                        save_posting_and_doc_collection(indexer,stem_outPath,posting_num)
                        #utils.save_obj(indexer.document_collection, os.path.join(stem_outPath, "document_collection_"+ str(posting_num)))
                        #utils.save_obj(indexer.postingDictAF, os.path.join(stem_outPath, "postingAF_" + str(posting_num)))
                        #utils.save_obj(indexer.postingDictGP, os.path.join(stem_outPath, "postingGP_" + str(posting_num)))
                        #utils.save_obj(indexer.postingDictQZ, os.path.join(stem_outPath, "postingQZ_" + str(posting_num)))
                        #utils.save_obj(indexer.postingDictSimbol,
                        #               os.path.join(stem_outPath, "postingSimbol_" + str(posting_num)))

                        indexer.init_posting()
                        posting_num += 1
                        num_doc_topost = 0

                    print("num of doc:", number_of_documents)

                    if number_of_documents == 500000:
                        break
            if number_of_documents == 500000:
                break
        if number_of_documents == 500000:
            break
    print(posting_num)

    save_posting_and_doc_collection(indexer,stem_outPath,posting_num)

    #indexer.sorted_inverted()
    utils.save_obj(sorted_dic_by_key(indexer.inverted_idx), os.path.join(stem_outPath, "inverted_idx"))

    print('Finished parsing and indexing. Starting to export files')

    return number_of_documents,posting_num


#def load_index(name_index):
#    print('Load inverted index')
#    inverted_index = utils.load_obj(name_index)
#    return inverted_index


def search_and_rank_query(query,inverted_index,document_collection,k,config,model):
    p = Parse(config)
    #parse the query ,return list of all the terms
    query_as_list = p.parse_sentence(query)[0]

    #searcher
    searcher = Searcher(inverted_index,document_collection,config)
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list,model) #, query_tf = searcher.relevant_docs_from_posting(query_as_list,model)
    print(len(relevant_docs))
    #calc the freq of query and the vector of the query
    query_tf = searcher.freq_terms_query(query_as_list)
    vec_query = searcher.avg_vector(query_tf.keys(),model)

    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs,query_tf,vec_query)
    return searcher.ranker.retrieve_top_k(ranked_docs, k)


def main(corpus_path=r"C:\Users\lazrati\Desktop\leeStudy\Data\Data",output_path=r"C:\Users\lazrati\Desktop\leeStudy\Data",stemming=False,queries=r"C:\Users\lazrati\Desktop\leeStudy\IR\queries.txt",num_doc_to_retrive=2000):
    now = datetime.now()

    config = ConfigClass()
    config.corpusPath = corpus_path
    config.savedFileMainFolder = output_path
    config.toStem = stemming

    corpus_num_docs,posting_num = run_engine(config)
    now_after_all = datetime.now()
    print("Diff Time parse =", now_after_all-now)

    now = datetime.now()
    main_merge(config.get__outputPath(), posting_num)
    now_after_all = datetime.now()
    print("Diff Time after mearge =", now_after_all-now)

    config.number_of_documents = corpus_num_docs
    #config.number_of_documents = 500000
    #query = input("Please enter a query: ")
    queries = ["Dr. Anthony Fauci wrote in a 2005 paper published in Virology Journal that hydroxychloroquine was effective in treating SARS.",
"The seasonal flu kills more people every year in the U.S. than COVID-19 has to date.",
"Coronavirus is less dangerous than the flu",
"The coronavirus pandemic is a cover for a plan to implant trackable microchips and that the Microsoft co-founder Bill Gates is behind it",
"Microsoft co-founder Bill Gates said \"only the people who have all the vaccines will still be able to move freely\".",
"Bill Gates owns the patent and vaccine for coronavirus.",
"Herd immunity has been reached.",
"Children are \“almost immune from this disease.\”",
"A study from the CDC and the WHO \“proves face masks do not prevent the spread of a virus.\”",
"hydroxychloroquine, zinc, and Zithromax can cure coronavirus",
"U.S. has \“one of the lowest mortality rates in the world\” from COVID-19",
"The spread of COVID-19 will slow down as the weather warms up",
"5G helps the spread of Covid-19",
"Injecting or consuming bleach or disinfectant can cure coronavirus",
"The COVID-19 pandemic was planned by the Rockefeller Foundation in \"Operation Lockstep.\"",
"COVID-19 could lose its epidemic status in the United States because of declining coronavirus death rates according to CDC data.",
"healthy people should NOT wear masks",
"coronavirus is a bioweapon created in a lab in Wuhan",
"The outbreak began because people ate bat soup",
"Outbreak people ate bat",
"coronavirus eat bat soup",
"Wearing a mask to prevent the spread of COVID-19 is unnecessary because the disease can also be spread via farts.",
"For younger people, seasonal flu is “in many cases” a deadlier virus than COVID-19.",
"The coronavirus disease (COVID-19) is caused by a virus",
"Covid-19 is not caused by bacteria",
"The prolonged use of medical masks when properly worn, DOES NOT cause CO2 intoxication nor oxygen deficiency",
"Masks don't cause CO2 intoxication.",
"The COVID-19 coronavirus pandemic caused a nationwide shortage of U.S. coins in circulation during the summer of 2020.",
"Coins shortage due to coronavirus",
"People should NOT wear masks while exercising"]

    #k = int(input("Please enter number of docs to retrieve: "))

    # limit the doc retrive to 2000
    if num_doc_to_retrive>2000:
        num_doc_to_retrive=2000

    if isinstance(queries, str):
        queries = list(
            filter(None, (line.rstrip() for line in open(r"C:\Users\lazrati\Desktop\leeStudy\IR\queries.txt",encoding="utf8"))))


    if queries:
        inverted_index = utils.load_inverted_index(os.path.join(config.get__outputPath(), "inverted_idx"))
        document_collection = utils.load_obj(os.path.join(config.get__outputPath(), "document_collection"))

        model = utils.load_GoogleNews_vectors_negative300('GoogleNews-vectors-negative300.bin')

        now_after_all = datetime.now()
        print("Diff Time after load googlenews =", now_after_all - now)
        with open('results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['query_id', 'tweet id', 'score'])
            #if isinstance(queries, list):
            for query in range(len(queries)):
                for doc_tuple in search_and_rank_query(queries[query], inverted_index,document_collection, num_doc_to_retrive,config,model):
                    print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
                    writer.writerow([query, doc_tuple[0], doc_tuple[1]])


        now_after_all = datetime.now()
        print("Diff Time after queries =", now_after_all - now)




