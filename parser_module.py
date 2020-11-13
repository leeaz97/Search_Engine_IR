from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document
import re
from urllib.parse import urlparse


class Parse:

    def __init__(self):
        self.stop_words = stopwords.words('english')

    def parse_hashtags(self , text):
        split_by_delimiter = []
        split_by_upper_letter =[ ]

        #extract word that start with hashtags and remove dedup
        hashtags_list = [ text[i]+text[i+1] for i, e in enumerate(text) if e == "#" and len(text) > i+1 ]
        #print(hashtags_list)

        #remove hashtag
        without_hashtag = [hashtag.replace('#', '') for hashtag in hashtags_list]
        #print(without_hashtag)

        # split by delimiter
        for s in without_hashtag:
            #there is at lest one delimiter '_'
            if '_' in s:
                for i in s.split('_'):
                    split_by_delimiter.append(i)
            #split by upper letter
            for i in re.sub(r'([A-Z]+)', r' \1', s).split():
                split_by_upper_letter.append(i)
        return split_by_delimiter+split_by_upper_letter+hashtags_list

    #how to consider 'http://www.cwi.nl:80/%7Eguido/Python.html'
    def parse_url(self ,url):
        u = urlparse(url)
        list_url = []
        if u.scheme:
            list_url.append(u.scheme)
        if u.netloc:
            list_url.append(u.netloc)
        if u.path.split("/"):
           [list_url.append(i) for i in u.path.split("/")]


        #print(u.scheme,u.netloc,u.path.split("/"),u.hostname,u.fragment,u.params,u.password,u.port,u.query,u.username)
        return list_url

    def parse_tags(self ,text):
        tags_list = [ text[i]+text[i+1] for i, e in enumerate(text) if e == "@" and len(text) > i+1 ]
        return tags_list

    def parse_percent(self ,text):
        return

    def parse_numbers_without_units(self ,text):
        #bigger than Thousand
        #bigger than Million
        #bigger than Billion
        return

    def parse_names_and_entities(self ,text):
        return

    def parse_LowerCaseOrUpperCase(self ,text):
        return

    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        print(text)
        text_tokens = word_tokenize(text)
        print(text_tokens)
        text_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]
        print(text_tokens_without_stopwords)
        if "#" in text_tokens:
            hashtags = self.parse_hashtags(text_tokens)
            print(hashtags)

        if "@" in text_tokens:
            tags = self.parse_tags(text_tokens)
            print(tags)
        #add all the func to tokanizer
        return text_tokens_without_stopwords

    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url = doc_as_list[3]
        indices = doc_as_list[4]
        retweet_text = doc_as_list[5]
        retweet_url = doc_as_list[6]
        retweet_indices = doc_as_list[7]
        quote_text = doc_as_list[8]
        quote_url = doc_as_list[9]
        quoted_indices = doc_as_list[10]
        retweet_quoted_text = doc_as_list[11]
        retweet_quoted_urls = doc_as_list[12]
        retweet_quoted_indices = doc_as_list[13]

        term_dict = {}
        tokenized_text = self.parse_sentence(full_text)

        print(type(url))
        #for item in url.items():
        #    tokenized_url = self.parse_url(url)
        #    print(tokenized_url)



        doc_length = len(tokenized_text)  # after text operations.

        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        document = Document(tweet_id, tweet_date, full_text, url, indices, retweet_text, retweet_url,
                            retweet_indices, quote_text, quote_url, quoted_indices, retweet_quoted_text,
                            retweet_quoted_urls, retweet_quoted_indices, term_dict, doc_length)
        return document
