from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document
import re
from urllib.parse import urlparse
import string
import spacy
sp = spacy.load('en_core_web_sm')

class Parse:

    def __init__(self):
        self.stop_words = stopwords.words('english')

    def remove_punctuation(self,text):
        without_punc = []
        for w in text:
            t = w.translate(str.maketrans('', '', string.punctuation))
            if t:
                without_punc.append(t)
        #x = [''.join(c for c in s if c not in string.punctuation) for s in text]
        return without_punc

    def parse_hashtags(self , text):
        split_by_delimiter = []
        split_by_upper_letter =[ ]

        #extract word that start with hashtags
        hashtags_list = [ text[i]+text[i+1] for i, e in enumerate(text) if e == "#" and len(text) > i+1 ]

        #remove hashtag
        without_hashtag = [hashtag.replace('#', '') for hashtag in hashtags_list]

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

    def parse_tags(self ,text):
        #list_tags = re.findall('^@^#[A-Za-z0-9_-]+', text)
        tags_list = [ text[i]+text[i+1] for i, e in enumerate(text) if e == "@" and len(text) > i+1 ]
        return tags_list

    #def parse_dollar(self ,text):
    #    dollar_start_list = re.findall(r'^\$(\d[\d., ]*?)\s', text)
    #    dollar_end_list = re.findall(r'(\d[\d., ]*?)\$$\s', text)
    #    #dollar_list = [text[i-1] + text[i] for i, e in enumerate(text) if e == "$" and i-1 > 0 ]
    #    return dollar_start_list + dollar_end_list

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
                    n_list.append(str(i))
                # bigger than Thousand
                elif i >= 1000 and i < 1000000:
                    if isinstance(i,int):
                        n_list.append(str(int(i/1000))+"K")
                    else:
                        n_list.append(str(i/1000)+"K")
                # bigger than Million
                elif i >= 1000000 and i < 1000000000:
                    if isinstance(i,int):
                        n_list.append(str(int(i/1000))+"M")
                    else:
                        n_list.append(str(i/1000000)+"M")
                #bigger than Billion
                else:
                    if isinstance(i,int):
                        n_list.append(str(int(i/1000))+"B")
                    else:
                        n_list.append(str(i/1000000000)+"B")
            else:
                n_list.append(str(i))
        return n_list

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

    def decontracted(self ,phrase):
        phrase = re.sub(r"\’", "\'", phrase)
        phrase = re.sub(r"\“", "\"", phrase)
        phrase = re.sub(r"\…", "...", phrase)

        # specific
        phrase = re.sub(r"won\'t", "will not", phrase)
        phrase = re.sub(r"can\'t", "can not", phrase)

        # general
        phrase = re.sub(r"n\'t", " not", phrase)
        phrase = re.sub(r"\'re", " are", phrase)
        phrase = re.sub(r"\'s", " is", phrase)
        phrase = re.sub(r"\'d", " would", phrase)
        phrase = re.sub(r"\'ll", " will", phrase)
        phrase = re.sub(r"\'t", " not", phrase)
        phrase = re.sub(r"\'ve", " have", phrase)
        phrase = re.sub(r"\'m", " am", phrase)
        return phrase

    def text2int(self, textnum, numwords={}):
        if not numwords:
            units = [
                "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
                "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                "sixteen", "seventeen", "eighteen", "nineteen",
            ]

            tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

            scales = ["hundred", "thousand", "million", "billion", "trillion"]

            numwords["and"] = (1, 0)
            for idx, word in enumerate(units):  numwords[word] = (1, idx)
            for idx, word in enumerate(tens):       numwords[word] = (1, idx * 10)
            for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)

        ordinal_words = {'first': 1, 'second': 2, 'third': 3, 'fifth': 5, 'eighth': 8, 'ninth': 9, 'twelfth': 12}
        ordinal_endings = [('ieth', 'y'), ('th', '')]

        textnum = textnum.replace('-', ' ')

        current = result = 0
        curstring = ""
        onnumber = False
        for word in textnum.split():
            if word.lower() in ordinal_words:
                scale, increment = (1, ordinal_words[word.lower()])
                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
                onnumber = True
            else:
                for ending, replacement in ordinal_endings:
                    if word.lower().endswith(ending):
                        word = "%s%s" % (word.lower()[:-len(ending)], replacement)

                if word.lower() not in numwords:
                    if onnumber:
                        curstring += repr(result + current) + " "
                    curstring += word + " "
                    result = current = 0
                    onnumber = False
                else:
                    scale, increment = numwords[word.lower()]

                    current = current * scale + increment
                    if scale > 100:
                        result += current
                        current = 0
                    onnumber = True

        if onnumber:
            curstring += repr(result + current)

        return curstring

    def parse_percent(self ,text):
        #conseder +\-
        text_after_percentage = re.sub(r'(\d[\d., ]*?)\spercentage[s]{0,1}', "\\1%", text)
        text_after_percent = re.sub(r'(\d[\d.,]*?)\spercent[s]{0,1}', "\\1%", text_after_percentage)
        return text_after_percent

    def parse_dollar_word(self,text):
        text_after_dollar = re.sub(r'(\d[\d., ]*?)\sdollar[s]{0,1}', "\\1$", text)
        #d_list = re.findall(r'\d[\d.,\s]*?dollar[s]*]', text)
        #for n in d_list:
        #    if "dollar" in n.lower():
        #        dollar_list.append(re.sub(r'[\s]*dollar[s]*', '$', n))
        #    else:
        #        dollar_list.append(n)
        return text_after_dollar

    def remove_Emojify(self,text):
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

        remove_emoji = emoji_pattern.sub(r'', text)
        return remove_emoji

    #def extract_expressions(self):
    #    expressions = re.findall('\'.*\'?|\".*\"|\`.*\`?|')
    #    return

    def parse_names_and_entities(self ,sen):
        '''In spacy have many label of entities we want just some of them ...
        ORG - Companies, agencies, institutions, etc.
        GPE - Countries, cities, states
        PERSON - People, including fictional
        NORP - Nationalities or religious or political groups
        LOC - Non-GPE locations, mountain ranges, bodies of water
        WORK_OF_ART - Titles of books, songs, etc.
        FAC - Buildings, airports, highways, bridges, etc.
        EVENT - Named hurricanes, battles, wars, sports events, etc.
        LANGUAGE - Any named language.
        #MISC - Miscellaneous entities, e.g. events, nationalities, products or works of art.'''

        label_list = ["ORG","GPE","PERSON","NORP","LOC","WORK_OF_ART","FAC","EVENT","LANGUAGE","MISC"]
        entity_list = []

        for entity in sen.ents:
            if entity.label_ in label_list and (not str(entity).startswith("@")):
                entity_list.append(entity)
        #print(entity.text + ' - ' + entity.label_ + ' - ' + str(spacy.explain(entity.label_)))
        return entity_list


    def remove_urlTwwit_from_text(self,text):
        t = re.sub(r'(https|http)?:\/\/t.co\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', text, flags=re.MULTILINE)
        #print(t)
        return t

    def parse_Date_and_time(self,sen):
        label_list = ["DATE","TIME"]
        entity_list = []

        for entity in sen.ents:
            if entity.label_ in label_list:
                entity_list.append(entity)
        # print(entity.text + ' - ' + entity.label_ + ' - ' + str(spacy.explain(entity.label_)))
        return entity_list

    def parse_LowerCaseOrUpperCase(self ,text):
        return

    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        hashtags=[]
        tags=[]
        text_tokens_split=[]

        remove_emoji = self.remove_Emojify(text)
        replace_word_to_num = self.text2int(remove_emoji)
        remove_and = re.sub(r'\s0\s', " ", replace_word_to_num)
        remove_url = self.remove_urlTwwit_from_text(remove_and)
        decontracted = self.decontracted(remove_url)

        #print("Text",text)
        #print("remove emoje",remove_emoji)
        #print("Replace_word_to_Num",replace_word_to_num)
        #print("Remove and", remove_and)
        #print("Remove decontracted", decontracted)

        #"%" in text or
        if "percent" in decontracted or "percentage" in decontracted:
            decontracted = self.parse_percent(decontracted)
         #   print("remove precent",decontracted)

        if "dollar" in decontracted:
            decontracted = self.parse_dollar_word(decontracted)
        #    print("remove dollar",decontracted)

        text_tokens = word_tokenize(decontracted)
        for i in text_tokens:
            if "/" in i:
                for j in i.split("/"):
                    text_tokens_split.append(j)
            else:
                text_tokens_split.append(i)
        #text_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]
        text_tokens_without_stopwords = [w for w in text_tokens_split if w not in self.stop_words]
        #print("token", text_tokens)
        #print("token without_stopwords", text_tokens_without_stopwords)

        #if "$" in text_tokens:
        #    d = self.parse_dollar(decontracted)
        #    print("Text", text)
        #    print("dollar", d)

        if "#" in text_tokens:
            hashtags = self.parse_hashtags(text_tokens_without_stopwords)
         #   print( "hashtags" ,hashtags)

        if "@" in text_tokens:
            tags = self.parse_tags(text_tokens_without_stopwords)
         #   print("tags" , tags)

        text_tokens_without_stopwords = self.num_Billion_Million_Thousand(text_tokens_without_stopwords)
        #if text_tokens_without_stopwords:
        #    print("big num",text_tokens_without_stopwords)

        remove_punctuation = self.remove_punctuation(text_tokens_without_stopwords)
        #if remove_punctuation:
        #    print("remove_punctuation",remove_punctuation)


        sen = sp(decontracted)
        names_and_entities = self.parse_names_and_entities(sen)
        date_and_time = self.parse_Date_and_time(sen)
        #print("names_and_entities",names_and_entities)
        #print("--------------------------------------------------------------------------------------")

        return remove_punctuation + names_and_entities + tags + hashtags + date_and_time

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
        tokenized_retweet_text=[]
        tokenized_retweet_quoted_text=[]
        tokenized_url=[]
        tokenized_retweet_url=[]
        tokenized_retweet_quoted_urls=[]

        tokenized_text = self.parse_sentence(full_text)
        if tokenized_retweet_text:
            tokenized_retweet_text = self.parse_sentence(retweet_text)
        if tokenized_retweet_quoted_text:
            tokenized_retweet_quoted_text = self.parse_sentence(retweet_quoted_text)
        if tokenized_url:
            tokenized_url = self.parse_url(url)
        if tokenized_retweet_url:
            tokenized_retweet_url = self.parse_url(retweet_url)
        if tokenized_retweet_quoted_urls:
            tokenized_retweet_quoted_urls = self.parse_url(retweet_quoted_urls)


        #print(full_text)
        #print(tokenized_text)
        #print("---------------------------------------------------------------------")
        full_tokenized = tokenized_text.extend(tokenized_retweet_text).extend(tokenized_retweet_quoted_text).extend(tokenized_url).extend(tokenized_retweet_url).extend(tokenized_retweet_quoted_urls)

        doc_length = len(full_tokenized)  # after text operations.

        for term in full_tokenized:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        document = Document(tweet_id, tweet_date, full_text, url, indices, retweet_text, retweet_url,
                            retweet_indices, quote_text, quote_url, quoted_indices, retweet_quoted_text,
                            retweet_quoted_urls, retweet_quoted_indices, term_dict, doc_length)
        return document
