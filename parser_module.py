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

        #extract word that start with hashtags
        # hashtags_list = re.findall('^#[A-Za-z0-9_-]+', text)
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
        list_url = []

        #split the string to list
        for i in url.split(','):
            #extract each url to group , group 1 is the shorted url , group 2 is the full url
            extract_full_url = re.search('{?"(.*)":(.*)', i)
            if extract_full_url:
                url_f = extract_full_url.group(2).replace("\"","").replace("}","")
                # if have full url
                if url_f != 'null':
                    # parse url with library urlparse
                    u = urlparse(url_f)
                    if u.scheme:
                        list_url.append(u.scheme)
                    if u.netloc:
                        list_url.append(u.netloc)
                    if u.path.split("/"):
                        for i in u.path.split("/"):
                            if i != '':
                                list_url.append(i)

        #print(u.scheme,u.netloc,u.path.split("/"),u.hostname,u.fragment,u.params,u.password,u.port,u.query,u.username)
        return list_url

    def parse_tags(self ,text):
        #list_tags = re.findall('^@^#[A-Za-z0-9_-]+', text)
        tags_list = [ text[i]+text[i+1] for i, e in enumerate(text) if e == "@" and len(text) > i+1 ]
        return tags_list

    def parse_percent(self ,text):
        percent_list = []
        #p_list = re.findall(r'\d[\d.,]*?[%|percentage|percent]{1}', text)
        p_list = re.findall(r'\d[\d.,\s]*?%|\d[\d.,\s]*?percentage|\d[\d.,\s]*?percent', text)

        for p in p_list:
           if "percentage" in p:
               percent_list.append(re.sub(r'[\s]*percentage', '%', p))
           elif "percent" in p:
               percent_list.append(re.sub(r'[\s]*percent', '%', p))
           elif "%" in p:
               percent_list.append(p)

        return percent_list

    def word_Billion_Million_Thousand(self, text):
        Billion_Million_Thousand_list = []
        n_list = re.findall(r'\d[\d.,\s]*?billion|\d[\d.,\s]*?million|\d[\d.,\s]*?thousand', text)

        for n in n_list:
           if "billion" in n:
               Billion_Million_Thousand_list.append(re.sub(r'[\s]*billion', 'B', n))
           elif "million" in n:
               Billion_Million_Thousand_list.append(re.sub(r'[\s]*million', 'M', n))
           elif "thousand" in n:
               Billion_Million_Thousand_list.append(re.sub(r'[\s]*thousand', 'K', n))


        return Billion_Million_Thousand_list


    def num_Billion_Million_Thousand(self, text):
        n_list = []
        for i in text:
            if re.match(r'^\d+$|^\d+?\.\d+?$|^\d+(\,+\d+)+$|^\d+(\,+\d+)+?\.\d+?$', i):
                if "," in i:
                    i = i.replace(",","")
                if "." in i:
                    i = float(i)
                else:
                    i = int(i)
                if i < 1000:
                    n_list.append(i)
                # bigger than Thousand
                elif i >= 1000 and i < 1000000:
                    #str(int(i/1000))
                    n_list.append(str(i/1000)+"K")
                # bigger than Million
                elif i >= 1000000 and i < 1000000000:
                    n_list.append(str(i/1000000)+"M")
                #bigger than Billion
                else:
                    n_list.append(str(i/1000000000)+"B")

        return n_list

    def delete_Emojify(self,text):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U0001F1F2-\U0001F1F4"  # Macau flag
                                   u"\U0001F1E6-\U0001F1FF"  # flags
                                   u"\U0001F600-\U0001F64F"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u"\U0001F1F2"
                                   u"\U0001F1F4"
                                   u"\U0001F620"
                                   u"\u200d"
                                   u"\u2640-\u2642"
                                   "]+", flags=re.UNICODE)

        text = emoji_pattern.sub(r'', text)
        return text

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
        print(self.delete_Emojify(text))
        print(text)
        print("---------------------------------")
        #print(text)
        text_tokens = word_tokenize(text)
        #print(text_tokens)
        text_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]
        #print(text_tokens_without_stopwords)
        if "#" in text_tokens:
            hashtags = self.parse_hashtags(text_tokens)
         #   print(hashtags)

        if "@" in text_tokens:
            tags = self.parse_tags(text_tokens)
          #  print(tags)

        if "%" in text or "percent" in text or "percentage" in text:
            #print(text)
            #print(text_tokens)
            #print(self.parse_percent(text))
            #print("-----------------")
            percent = self.parse_percent(text)

        if "billion" in text or "million" in text or "thousand" in text:
            big_num_word = self.word_Billion_Million_Thousand(text)

        if self.num_Billion_Million_Thousand(text_tokens):
            #print(text)
            #print(self.num_Billion_Million_Thousand(text_tokens))
            big_num = self.num_Billion_Million_Thousand(text_tokens)
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

        #print(type(url))
        tokenized_url = self.parse_url(url)
        #print(tokenized_url)



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
