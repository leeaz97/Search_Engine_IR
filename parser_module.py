import re
from urllib.parse import urlparse
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize.regexp import regexp_tokenize
from document import Document
from stemmer import Stemmer
import math
import keras_preprocessing.text as keras_t
from nltk.stem.wordnet import WordNetLemmatizer

sp = spacy.load('en_core_web_sm')

class Parse:

    def __init__(self, config):
        #config = ConfigClass()
        self.stop_words = stopwords.words('english')
        self.stemmer = config.toStem


    #def wordNet(self,text):
    #    #words = ['gave', 'went', 'going', 'dating']
    #    for word in text:
    #        print(word + "-->" + WordNetLemmatizer().lemmatize(word, 'v'))

    def remove_punctuation(self,text):
        without_punc = []
        for w in text:
            if not re.match(r'^\d', w ):
                #t = w.translate(str.maketrans('', '', string.punctuation))
                t = w.translate(str.maketrans('', '', r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""))
            else:
                t=w
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

    def parse_percent(self,text):
        list_percent = re.findall(r'(\d[\d., ]*?%)\s*',text)
        return list_percent

    def parse_dollar(self ,text):
        start_dollar = re.findall(r'(\$\d[\d., ]*)',text)
        end_dollar = re.findall(r'(\d[\d., ]*?\$)\s*',text)
        return start_dollar + end_dollar

    def num_Billion_Million_Thousand(self, text):
        # do modole %
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
                elif 1000000 <= i < 1000000000:
                    #print(i,type(i),i%1000)
                    if i % 1000 == 0:
                        n_list.append(str(int(i/1000))+"K")
                    else:
                        n_list.append(str(float(i/1000))+"K")
                # bigger than Million
                elif i >= 1000000 and i < 1000000000:
                    if i % 1000000 == 0:
                        n_list.append(str(int(i/1000000))+"M")
                    else:
                        n_list.append(str(float(i/1000000))+"M")
                #bigger than Billion
                else:
                    if i % 1000000000 == 0:
                        n_list.append(str(int(i/1000000000))+"B")
                    else:
                        n_list.append(str(float(i/1000000000))+"B")
            else:
                n_list.append(str(i))
        return n_list

    #how to consider 'http://www.cwi.nl:80/%7Eguido/Python.html'
    def parse_url(self ,url):
        #print(url)
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
        phrase = re.sub(r"\”", "\"", phrase)
        phrase = re.sub(r"\‘", "\'", phrase)


        # specific
        phrase = re.sub(r"won\'t", "will not", phrase)
        phrase = re.sub(r"can\'t", "can not", phrase)
        phrase = re.sub(r"don\'t", "do not", phrase)
        phrase = re.sub(r"doesn\'t", "does not", phrase)

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

    def parse_percent_word(self ,text):
        text_after_percentage = re.sub(r'(\d[\d.,]*?)\s?percent(age)*[s]{0,1}', "\\1%", text)
        #conseder +\-
        #text_after_percentage = re.sub(r'(\d[\d.,]*?)\spercentage[s]{0,1}', "\\1%", text)
        #text_after_percent = re.sub(r'(\d[\d.,]*?)\spercent[s]{0,1}', "\\1%", text_after_percentage)
        return text_after_percentage

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
                                   u"\u2069"
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
                                   u"\u1F637"
                                   "❤"
                                   "😷"
                                   "❤"
                                   "❤😷"
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
        MISC - Miscellaneous entities, e.g. events, nationalities, products or works of art.'''

        label_list = ["ORG","GPE","PERSON","NORP","LOC","WORK_OF_ART","FAC","EVENT","LANGUAGE","MISC"]
        entity_list = []

        for entity in sen.ents:
            if entity.label_ in label_list and (not str(entity).startswith("@")) and (not str(entity).startswith("RT @")):
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

    def parse_LowerCaseOrUpperCase(self,tokens):
        #tokens = ['wear', 'a', 'lee', 'Wear', 'Done']
        l = []
        for x in tokens:
            if x.lower() in tokens:
                l.append(x.lower())
            else:
                l.append(x)
        return l

    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        hashtags=[]
        tags=[]
        dollar=[]
        percent=[]
        text_tokens_split=[]

        #remove_emoji = self.remove_Emojify(text)
        #replace_word_to_num = self.text2int(remove_emoji)
        #remove_and = re.sub(r'\s0\s', " ", remove_emoji)
        remove_url = self.remove_urlTwwit_from_text(text)
        decontracted = self.decontracted(remove_url)

        # clean_text
        decontracted = re.sub('[^a-zA-Z0-9-!@\\\$%\^&*{}\[\]|/\'\":;><.,`~?\#]+', r" ", decontracted)
        #print(decontracted)

        #"%" in text or
        if "percent" in decontracted or "percentage" in decontracted:
            decontracted = self.parse_percent_word(decontracted)
         #   print("remove precent",decontracted)

        if "dollar" in decontracted:
            decontracted = self.parse_dollar_word(decontracted)
        #    print("remove dollar",decontracted)

        if "$" in decontracted:
            dollar = self.parse_dollar(decontracted)

        if "%" in decontracted:
            percent = self.parse_percent(decontracted)
        #print("txt: ", decontracted)
        # replacing versions of covid to "covid"
        # decontracted = re.sub("(?i)[a-zA-Z]?covid[a-zA-Z]?-?~?_?1?9?[a-zA-Z]?|(?i)[a-zA-Z]?corona[a-zA-Z]?-?~?_?1?9?[a-zA-Z]?", r"covid", decontracted, flags=re.IGNORECASE)
        #
        # replacing fractions to rationals
        decontracted = re.sub("(\d+) (\d+)/(\d+)",
                              lambda x: "{:.2f}".format((int(x.group(1))) + (float(x.group(2)) / int(x.group(3)))),
                              decontracted,
                              flags=re.IGNORECASE)
        decontracted = re.sub("(\d+)/(\d+)", lambda x: "{:.2f}".format(int(x.group(1)) / int(x.group(2))), decontracted,
                              flags=re.IGNORECASE)
        s_covid = '((?i)^([#@]+)[.]*covid[.]*virus?-?~?_?\'?1?9?[.]*)'
        s_coron = '((?i)^([#@]+)[.]*corona[.]*virus?-?~?_?\'?1?9?[a-zA-Z]*)'
        #s_frach = re.compile(r'(\d+) (\d+)/(\d+)')
        #s_frac = re.compile(r'(\d+)/(\d+)')
        abc = re.compile(s_covid + '|' + s_coron)
        i = 0
        for ma in re.finditer(abc, decontracted):
            i += 1
            # print (i,": ",ma.groups())
            if (ma.group(1)):
                print("1", ma.group(1))
                decontracted = decontracted.replace(ma.group(1), "covid")
                # re.sub(ma, "covid")
            if (ma.group(2)):
                print("2", ma.group(2))
                decontracted = decontracted.replace(ma.group(2), "covid")

        # print("covid: ", decontracted)
        # text_tokens = word_tokenize(decontracted)
        text_tokens = keras_t.text_to_word_sequence(decontracted, filters='.()*+=:;\"`<>!?“[]}{\n\t', lower=False,
                                                    split=" ")
        # remove
        # text_tokens=re.sub("^&\d?", "", text_tokens)

        # text_regex = regexp_tokenize(decontracted, pattern="[ .():;\"<>!?“\[\]}{\n\t]", gaps=True)
        # text_token_keras = keras_t.text_to_word_sequence(decontracted)
        # print("nltk: ", text_tokens)
        #print("keras: ", text_tokens)
        #text_tokens = word_tokenize(decontracted)
        #print(text_tokens)

        for i in text_tokens:
            if "/" in i:
                for j in i.split("/"):
                    text_tokens_split.append(j)
            else:
                text_tokens_split.append(i)

        #text_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]
        text_tokens_without_stopwords = [w for w in text_tokens_split if w.lower() not in self.stop_words]
        #print("token", text_tokens)
        #print("token without_stopwords", text_tokens_without_stopwords)

        if "#" in text_tokens:
            hashtags = self.parse_hashtags(text_tokens_without_stopwords)
         #   print( "hashtags" ,hashtags)

        if "@" in text_tokens:
            tags = self.parse_tags(text_tokens_without_stopwords)
         #   print("tags" , tags)

        text_tokens_without_stopwords = self.num_Billion_Million_Thousand(text_tokens_without_stopwords)
        #if text_tokens_without_stopwords:
        #    print("big num",text_tokens_without_stopwords)

        remove_upper_exist = self.parse_LowerCaseOrUpperCase(text_tokens_without_stopwords)

        remove_punctuation = self.remove_punctuation(remove_upper_exist)
        #if remove_punctuation:
        #    print("remove_punctuation",remove_punctuation)


        sen = sp(decontracted)
        names_and_entities = self.parse_names_and_entities(sen)
        date_and_time = self.parse_Date_and_time(sen)
        #print("names_and_entities",names_and_entities)
        #print("--------------------------------------------------------------------------------------")
        # insert the new name and entities to the token list
        for e in names_and_entities:
            #search if not exists in tokens
            if str(e) not in remove_punctuation:
                remove_punctuation.append(str(e))
        # insert the new date\time to the token list
        for e in date_and_time:
            # search if not exists in tokens
            if str(e) not in remove_punctuation:
                remove_punctuation.append(str(e))

        full_tokens = remove_punctuation + tags + hashtags + dollar + percent

        #remove_punctuation + names_and_entities + tags + hashtags + date_and_time
        return (full_tokens,len(remove_punctuation))


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
        #term_dict_stemming = {}
        tokenized_retweet_text=[]
        tokenized_retweet_quoted_text=[]
        tokenized_url=[]
        tokenized_retweet_url=[]
        tokenized_retweet_quoted_urls=[]
        doc_length = 0
        max_tf = 0

        if full_text:
            #return tuple , in place o - tokens list ,in place 1 - len of terms
            tokenized_text_1 = self.parse_sentence(full_text)
            tokenized_text = tokenized_text_1[0]
            doc_length += tokenized_text_1[1]

        if retweet_text:
            tokenized_retweet_text_1 = self.parse_sentence(retweet_text)
            tokenized_retweet_text = tokenized_retweet_text_1[0]
            doc_length += tokenized_retweet_text_1[1]

        if retweet_quoted_text:
            tokenized_retweet_quoted_text_1 = self.parse_sentence(retweet_quoted_text)
            tokenized_retweet_quoted_text = tokenized_retweet_quoted_text_1[0]
            doc_length += tokenized_retweet_quoted_text_1[1]

        if url:
            tokenized_url = self.parse_url(url)
            doc_length += len(tokenized_url)
        if retweet_url:
            tokenized_retweet_url = self.parse_url(retweet_url)
            doc_length += len(tokenized_retweet_url)
        if retweet_quoted_urls:
            tokenized_retweet_quoted_urls = self.parse_url(retweet_quoted_urls)
            doc_length += len(tokenized_retweet_quoted_urls)

        #print("---------------------------------------------------------------------")


        full_tokenized = tokenized_text + tokenized_retweet_text + tokenized_retweet_quoted_text
        urls_tokenized = tokenized_url + tokenized_retweet_url + tokenized_retweet_quoted_urls

        #Stemming
        if self.stemmer:
            s = Stemmer()
            full_tokenized = s.stem_term(full_tokenized)

        # Stemming for urls
        if self.stemmer:
            s = Stemmer()
            urls_tokenized = s.stem_term(urls_tokenized)

        #print("Stemming",self.stemmer)

        for term in full_tokenized:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        for term in urls_tokenized:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        #max_tf the max frequnce of term in doc
        if term_dict:
            max_tf = max(term_dict.values())

        #print(full_text)
        #print(term_dict)

        if term_dict:
            nf = 1/math.sqrt(sum(pow(item,2) for item in term_dict.values()))

            #avg_veactor_toDoc(model, parsed_document)

            document = Document(tweet_id, tweet_date, full_text, url, indices, retweet_text, retweet_url,
                                retweet_indices, quote_text, quote_url, quoted_indices, retweet_quoted_text,
                                retweet_quoted_urls, retweet_quoted_indices, term_dict, doc_length ,max_tf ,nf)


            return document
        else:
            return None
