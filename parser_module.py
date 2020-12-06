import regex as re
from urllib.parse import urlparse
import math
# import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize.regexp import regexp_tokenize

from document import Document
from stemmer import Stemmer


import keras_preprocessing.text as keras_t
# define the document
# tokenize the document

# sp = spacy.load('en_core_web_sm')


class Parse:

    def __init__(self, config):
        # config = ConfigClass()
        self.stop_words = stopwords.words('english')
        self.stemmer = config.toStem

    # def wordNet(self,text):
    #    #words = ['gave', 'went', 'going', 'dating']
    #    for word in text:
    #        print(word + "-->" + WordNetLemmatizer().lemmatize(word, 'v'))

    def remove_punctuation(self, text):
        without_punc = []
        for w in text:
            if not re.match(r'^\d', w):
                # t = w.translate(str.maketrans('', '', string.punctuation))
                t = w.translate(str.maketrans('', '', r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""))
            else:
                t = w
            if t:
                without_punc.append(t)
        # x = [''.join(c for c in s if c not in string.punctuation) for s in text]
        return without_punc

    def parse_hashtags(self, text):
        split_by_delimiter = []
        split_by_upper_letter = []

        # extract word that start with hashtags
        hashtags_list = [text[i] + text[i + 1] for i, e in enumerate(text) if e == "#" and len(text) > i + 1]

        # remove hashtag
        without_hashtag = [hashtag.replace('#', '') for hashtag in hashtags_list]

        # split by delimiter
        for s in without_hashtag:
            # there is at lest one delimiter '_'
            if '_' in s:
                for i in s.split('_'):
                    split_by_delimiter.append(i)
            # split by upper letter
            for i in re.sub(r'([A-Z]+)', r' \1', s).split():
                split_by_upper_letter.append(i)
        return split_by_delimiter + split_by_upper_letter + hashtags_list

    def parse_tags(self, text):
        # list_tags = re.findall('^@^#[A-Za-z0-9_-]+', text)
        tags_list = [text[i] + text[i + 1] for i, e in enumerate(text) if e == "@" and len(text) > i + 1]
        return tags_list

    def parse_percent(self, text):
        list_percent = re.findall(r'(\d[\d., ]*?%)\s*', text)
        return list_percent

    def parse_dollar(self, text):
        start_dollar = re.findall(r'(\$\d[\d., ]*)', text)
        end_dollar = re.findall(r'(\d[\d., ]*?\$)\s*', text)
        return start_dollar + end_dollar

    def num_Billion_Million_Thousand(self, text):
        # do modole %
        n_list = []
        for i in text:

            # decontracted = re.sub((r"[-+]?\d*[/\\]\d+", decontracted))
            if re.match(r'^\d+$|^\d+?\.\d+?$|^\d+(,+\d+)+$|^\d+(,+\d+)+?\.\d+?$', i):
                if "," in i:
                    i = i.replace(",", "")
                if "." in i:
                    i = float(i)
                else:
                    i = int(i)
                if i < 1000:
                    n_list.append(str(i))
                # bigger than Thousand
                elif i >= 1000 and i < 1000000:
                    # print(i,type(i),i%1000)
                    if i % 1000 == 0:
                        n_list.append(str(int(i / 1000)) + "K")
                    else:
                        n_list.append(str(float(i / 1000)) + "K")
                # bigger than Million
                elif 1000000 <= i < 1000000000:
                    if i % 1000000 == 0:
                        n_list.append(str(int(i / 1000000)) + "M")
                    else:
                        n_list.append(str(float(i / 1000000)) + "M")
                # bigger than Billion
                else:
                    if i % 1000000000 == 0:
                        n_list.append(str(int(i / 1000000000)) + "B")
                    else:
                        n_list.append(str(float(i / 1000000000)) + "B")
            else:
                n_list.append(str(i))
        return n_list

    def parse_url(self, url):
        # print(url)
        list_url = []
        # split the string to list
        for i in url.split(','):
            # extract each url to group , group 1 is the shorted url , group 2 is the full url
            extract_full_url = re.search('{?"(.*)":(.*)', i)
            if extract_full_url:
                url_f = extract_full_url.group(2).replace("\"", "").replace("}", "")
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
                                if '-' in i:
                                    for q in i.split('-'):
                                        list_url.append(q)
                                else:
                                    list_url.append(i)

        # print(u.scheme,u.netloc,u.path.split("/"),u.hostname,u.fragment,u.params,u.password,u.port,u.query,u.username)
        return list_url

    def decontracted(self, phrase):
        #for word in phrase:
        phrase = re.sub(r"\’", "\'", phrase,flags=re.IGNORECASE)
        phrase = re.sub(r"\“", "\"", phrase,flags=re.IGNORECASE)
        phrase = re.sub(r"\…", "...", phrase,flags=re.IGNORECASE)
        phrase = re.sub(r"\”", "\"", phrase,flags=re.IGNORECASE)
        phrase = re.sub(r"\‘", "\'", phrase,flags=re.IGNORECASE)

        # specific
        phrase = re.sub(r"won\'t", "will not", phrase,flags=re.IGNORECASE)
        phrase = re.sub(r"can\'t", "can not", phrase,flags=re.IGNORECASE)
        phrase = re.sub(r"don\'t", "do not", phrase,flags=re.IGNORECASE)
        phrase = re.sub(r"doesn\'t", "does not", phrase,flags=re.IGNORECASE)
        phrase = re.sub(r"haven \'t", "have not", phrase,flags=re.IGNORECASE)
        phrase = re.sub(r"(?i)i\'ve", "i have", phrase,flags=re.IGNORECASE)
        phrase = re.sub(r"(?i)im", "i am", phrase, flags=re.IGNORECASE)


        # general
        phrase = re.sub(r"n\'t", " not", phrase,flags=re.IGNORECASE)
        phrase = re.sub(r"\'re", " are", phrase,flags=re.IGNORECASE)
        phrase = re.sub(r"\'s", " is", phrase,flags=re.IGNORECASE)
        phrase = re.sub(r"\'d", " would", phrase,flags=re.IGNORECASE)
        phrase = re.sub(r"\'ll", " will", phrase,flags=re.IGNORECASE)
        phrase = re.sub(r"\'t", " not", phrase,flags=re.IGNORECASE)
        phrase = re.sub(r"\'ve", " have", phrase,flags=re.IGNORECASE)
        phrase = re.sub(r"\'m", " am", phrase,flags=re.IGNORECASE)
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

    def parse_names_and_entities(self, sen):
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

        label_list = ["ORG", "GPE", "PERSON", "NORP", "LOC", "WORK_OF_ART", "FAC", "EVENT", "LANGUAGE", "MISC"]
        entity_list = []

        for entity in sen.ents:
            if entity.label_ in label_list and (not str(entity).startswith("@")) and (
                    not str(entity).startswith("RT @")):
                entity_list.append(entity)
        # print(entity.text + ' - ' + entity.label_ + ' - ' + str(spacy.explain(entity.label_)))
        return entity_list

    def remove_urlTwwit_from_text(self, text):
        t = re.sub(r'(https|http)?:\/\/t.co\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', text, flags=re.MULTILINE)
        # print(t)
        return t

    def parse_Date_and_time(self, sen):
        label_list = ["DATE", "TIME"]
        entity_list = []

        for entity in sen.ents:
            if entity.label_ in label_list:
                entity_list.append(entity)
        # print(entity.text + ' - ' + entity.label_ + ' - ' + str(spacy.explain(entity.label_)))
        return entity_list

    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        hashtags = []
        tags = []
        dollar = []
        percent = []
        text_tokens_split = []

        #print("text1", text)
        #remove_emoji = self.remove_Emojify(text)
        # replace_word_to_num = self.text2int(remove_emoji)
        # remove_and = re.sub(r'\s0\s', " ", remove_emoji)
        #remove_url = self.remove_urlTwwit_from_text(text)

        #find entities
        # import regex as re
        # text = "The King cds Bibi King Of Israel sfdf Alexandria Ocasio-Cortez fdf"

        entiteis = re.findall("(?:[A-Z]\w*(?:\s|$|-)+)+", text)


        # clean_text from garbage chars
        decontracted = re.sub('[^a-zA-Z0-9-!\\\$%@#\?\^&*{}._\[\]|/\'\":;><,`~]+', r" ", text)

        # superate words with ends like: 't/'d
        decontracted = self.decontracted(decontracted)
        #("text2", decontracted)


        # replace all percentage to "%" in text
        decontracted = re.sub(r'(\d[\d.,]*?)\s?percent(age)*[s]{0,1}', "\\1%", decontracted)

        # replace all dollar to "$" in text
        decontracted = re.sub(r'(\d[\d., ]*?)\sdollar[s]{0,1}', "\\1$", decontracted)

        #create list of words with "$" in decontracted:
        start_dollar = re.findall(r'(\$\d[\d., ]*)', decontracted)
        end_dollar = re.findall(r'(\d[\d., ]*?\$)\s*', decontracted)
        dollar = start_dollar + end_dollar

        # create list of words with "%" in decontracted:
        percent = re.findall(r'(\d[\d., ]*?%)\s*', decontracted)

        # replacing all versions of COVID-19 to "covid"
        decontracted = re.sub("(?i)[a-zA-Z]*covid[a-zA-Z]*-?~?_?[0-9]*[a-zA-Z]?|(?i)[a-zA-Z]*corona[a-zA-Z]*-?~?_?[0-9]*[a-zA-Z]*", r"covid", decontracted, flags=re.IGNORECASE)

        # replacing fractions to rationals
        #fraction with integer
        decontracted = re.sub("(\d+) (\d+)/([1-9]+)",
                               lambda x: "{:.2f}".format((int(x.group(1))) + (float(x.group(2)) / int(x.group(3)))),
                               decontracted,
                               flags=re.IGNORECASE)
        #only fraction
        decontracted = re.sub("(\d+)/([1-9]+)", lambda x: "{:.2f}".format(int(x.group(1)) / int(x.group(2))), decontracted,
                               flags=re.IGNORECASE)
        #s_frach = re.compile(r'(\d+) (\d+)/(\d+)')
        #s_frac = re.compile(r'(\d+)/(\d+)')

        #extract tokens from text
        text_tokens = keras_t.text_to_word_sequence(decontracted, filters='()*+=:;\"`|/\\<>!?“[]}{\n\t', lower=False, split=" ")
        #print("token", text_tokens)

        # text_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]
        text_tokens = [w for w in text_tokens if w.lower() not in self.stop_words]

      #handelling hashtags, numbers
        itr=0
        for token in text_tokens:
            # itr = text_tokens.index(token)
            # handelling hashtags
            # save word without # hashtag
            # print(text_tokens[itr])
            if ("#" in token):
                text_tokens.append(token.replace('#', ''))
                end_itr=(len(text_tokens))-1
                #split by delimiter
                #there is at lest one delimiter '_'
                if '_' in text_tokens[end_itr]:
                    for w in text_tokens[end_itr].split('_'):
                        text_tokens.append(w)
                # split by upper letter
                token = re.sub("([A-Z]{2})([a-z])", r'\1 \2', token)
                token = re.sub("([a-z]{2})([A-Z])", r'\1 \2', token)

                flag=0
                #IDTwitter
                # for up_let in re.sub(r'([A-Z]+[A-Z][a-z]+)', r' \1', text_tokens[end_itr]).split():
                #     flag = 1
                #     text_tokens.append(up_let)

                for up_let in re.sub(r'([A-Z]+|[a-z]+)', r' \1', text_tokens[end_itr]).split():
                    flag=1
                    text_tokens.append(up_let)

                #split by upper/lower subwords
                if(flag==1):
                    for up_let in re.sub(r'([A-Z][a-z]+|[a-z][A-Z]+)', r' \1', text_tokens[end_itr]).split():
                        text_tokens.append(up_let)

            token = re.sub("(?<=^|[^\d])(\d{1,3}),?(\d{3})(\.\d+)?(?=$|[^\d])",
                                          lambda x: x.group(1) + ("." + x.group(2) if x.group(2) != "000" else "") + "K", token)
                # milions
            token = re.sub("(?<=^|[^\d])(\d{1,3}),?(\d{3}),?\d{3}(\.\d+)?(?=$|[^\d])",
                                          lambda x: x.group(1) + ("." + x.group(2) if x.group(2) != "000" else "") + "M", token)
                # Billion
            token = re.sub("(?<=^|[^\d])(\d{1,3}),?(\d{3}),?\d{3},?\d{3}(\.\d+)?(?=$|[^\d])",
                                          lambda x: x.group(1) + ("." + x.group(2) if x.group(2) != "000" else "") + "B", token)
            # remove words with 1 letter
            if (len(token) < 2):
                token=''
            else:

                #remove $ from words
                if (re.match(r'^\$[a-zA-Z]+|[aa-zA-Z]+\$[a-zA-Z]*',token)):
                    token = token.replace("$", '')
                # if (re.match('(?i)http|t.co', token)):
                #     text_tokens[itr] = ''
                if (re.match('[.]+[\w]|\w[.]+', token)):
                    token = token.replace(".", '')
                if (re.match(r'&[a-zA-Z]+', text_tokens[itr])):
                    token = token.replace("&", '')
        text_tokens = list(filter(None, text_tokens))

        # Stemming
        if self.stemmer:
            s = Stemmer()
            text_tokens = s.stem_term(text_tokens)

        # remove_punctuation + names_and_entities + tags + hashtags + date_and_time
        return (text_tokens+entiteis+dollar+percent, len(text_tokens))



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

        if term_dict:
            nf = 1/math.sqrt(sum(pow(item,2) for item in term_dict.values()))

            #avg_veactor_toDoc(model, parsed_document)

            document = Document(tweet_id, tweet_date, full_text, url, indices, retweet_text, retweet_url,
                                retweet_indices, quote_text, quote_url, quoted_indices, retweet_quoted_text,
                                retweet_quoted_urls, retweet_quoted_indices, term_dict, doc_length ,max_tf ,nf)


            return document
        else:
            return None
