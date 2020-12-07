import regex as re
import math
from nltk.corpus import stopwords
from document import Document
from stemmer import Stemmer
import keras_preprocessing.text as keras_t
import time


class Parse:

    def __init__(self, config):
        # config = ConfigClass()
        self.stop_words = stopwords.words('english')
        self.stemmer = config.toStem

    # def wordNet(self,text):
    #    #words = ['gave', 'went', 'going', 'dating']
    #    for word in text:
    #        print(word + "-->" + WordNetLemmatizer().lemmatize(word, 'v'))

    # how to consider 'http://www.cwi.nl:80/%7Eguido/Python.html'
    def parse_url(self, url):
        # split the string to list
        for i in url.split(','):
                     # extract each url to group , group 1 is the shorted url , group 2 is the full url
            extract_full_url = re.search('{?"(.*)":(.*)', i)
            if extract_full_url:
                url_f = extract_full_url.group(2).replace("\"", "").replace("}", "")
                         # if have full url
                if url_f != 'null':
                    # replacing all versions of COVID-19 to "covid"
                    url_f = re.sub(
                        "(?i)[a-zA-Z]*covid[a-zA-Z]*-?~?_?[0-9]*[a-zA-Z]?|(?i)[a-zA-Z]*corona[a-zA-Z]*-?~?_?[0-9]*[a-zA-Z]*",
                        r"Covid", url_f, flags=re.IGNORECASE)

                    # replacing all versions of donald trump to "Donald Trump"
                    url_f = re.sub(
                        "(?i)[a-zA-Z0-9]*donald[a-zA-Z0-9]*-?~?_?trump*[a-zA-Z0-9]?|(?i)[a-zA-Z0-9]*trump[a-zA-Z0-9]*-?~?_?donald*[a-zA-Z0-9]*",
                        r"Trump", url_f, flags=re.IGNORECASE)
                    list_url = keras_t.text_to_word_sequence(url_f, filters='()*+=:;\"`-_&#,~|\\<>!?“[]}{/\n//\t//', lower=False, split=" ")
                    list_url = [w for w in list_url if w.lower() not in self.stop_words]
                    return list_url

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

    def entities(self,text):
        entiteis=[]
        entiteis = re.findall("(?:[A-Z]\w*(?:\s|$|-)+)+", text) #([A-Z][\w']*(?:\s+[A-Z][\w']*)*)
        return entiteis

    def numbers(self,decontracted):
        # hendelling numbers
        num=[]
        num = re.sub("(?<=^|[^\d])(\d{1,3}\.\d+)(?=$|[^\d])",
                              lambda x: str(round(float(format(x.group(1))), 3)), decontracted)
        # thousands

        num = re.sub("(?<=^|[^\d])(\d{1,3}),?(\d{3})(\.\d+)?(?=$|[^\d])",
                              lambda x: x.group(1) + ("." + x.group(2) if x.group(2) != "000" else "") + "K",
                              decontracted)
        # milions
        num = re.sub("(?<=^|[^\d])(\d{1,3}),?(\d{3}),?\d{3}(\.\d+)?(?=$|[^\d])",
                              lambda x: x.group(1) + ("." + x.group(2) if x.group(2) != "000" else "") + "M",
                              decontracted)
        # Billion
        num = re.sub("(?<=^|[^\d])(\d{1,3}),?(\d{3}),?\d{3},?\d{3}(\.\d+)?(?=$|[^\d])",
                              lambda x: x.group(1) + ("." + x.group(2) if x.group(2) != "000" else "") + "B",
                              decontracted)
        return num


    def elset(self, decontracted):
        #list=[]

        # superate words with ends like: 't/'d
        decontracted = self.decontracted(decontracted)
        # ("text2", decontracted)

        # replacing all versions of COVID-19 to "covid"
        decontracted = re.sub(
            "(?i)[a-zA-Z]*covid[a-zA-Z]*-?~?_?[0-9]*[a-zA-Z]?|(?i)[a-zA-Z]*corona[a-zA-Z]*-?~?_?[0-9]*[a-zA-Z]*",
            r"Covid", decontracted, flags=re.IGNORECASE)

        # replacing all versions of donald trump to "Donald Trump"
        decontracted = re.sub(
            "(?i)[a-zA-Z0-9]*donald[a-zA-Z0-9]*-?~?_?trump*[a-zA-Z0-9]?|(?i)[a-zA-Z0-9]*trump[a-zA-Z0-9]*-?~?_?donald*[a-zA-Z0-9]*",
            r"Trump", decontracted, flags=re.IGNORECASE)

        # replace all percentage to "%" in text
        decontracted = re.sub(r'(\d[\d.,]*?)\s?percent(age)*[s]{0,1}', "\\1%", decontracted)

        # replace all dollar to "$" in text
        decontracted = re.sub(r'(\d[\d., ]*?)\sdollar[s]{0,1}', "\\1$", decontracted)

        return decontracted

    def parse_sentence(self, text):

        # This function tokenize, remove stop words and apply lower case for every word within the text


        # print("text1", text)


        # clean_text from garbage chars
        decontracted = re.sub('[^a-zA-Z0-9-!\\\$%@#\?\^&*{}._\[\]|/\":;><,`~]+', r" ", text)

        # entiteis = re.findall("(?:[A-Z]\w*(?:\s|$|-)+)+", text) #([A-Z][\w']*(?:\s+[A-Z][\w']*)*)

        entiteis=self.entities(text)

        #
        # # superate words with ends like: 't/'d
        # decontracted = self.decontracted(decontracted)
        # #("text2", decontracted)
        #
        # # replacing all versions of COVID-19 to "covid"
        # decontracted= re.sub(
        #     "(?i)[a-zA-Z]*covid[a-zA-Z]*-?~?_?[0-9]*[a-zA-Z]?|(?i)[a-zA-Z]*corona[a-zA-Z]*-?~?_?[0-9]*[a-zA-Z]*",
        #     r"Covid", decontracted, flags=re.IGNORECASE)
        #
        # # replacing all versions of donald trump to "Donald Trump"
        # decontracted = re.sub(
        #     "(?i)[a-zA-Z0-9]*donald[a-zA-Z0-9]*-?~?_?trump*[a-zA-Z0-9]?|(?i)[a-zA-Z0-9]*trump[a-zA-Z0-9]*-?~?_?donald*[a-zA-Z0-9]*",
        #     r"Trump", decontracted, flags=re.IGNORECASE)
        #
        # # replace all percentage to "%" in text
        # decontracted = re.sub(r'(\d[\d.,]*?)\s?percent(age)*[s]{0,1}', "\\1%", decontracted)
        #
        # # replace all dollar to "$" in text
        # decontracted = re.sub(r'(\d[\d., ]*?)\sdollar[s]{0,1}', "\\1$", decontracted)

        # # hendelling numbers
        # decontracted= re.sub("(?<=^|[^\d])(\d{1,3}\.\d+)(?=$|[^\d])",
        #                           lambda x: str(round(float(format(x.group(1))), 3)), decontracted)
        # # thousands
        #
        # decontracted = re.sub("(?<=^|[^\d])(\d{1,3}),?(\d{3})(\.\d+)?(?=$|[^\d])",
        #                           lambda x: x.group(1) + ("." + x.group(2) if x.group(2) != "000" else "") + "K",
        #                       decontracted)
        # # milions
        # decontracted = re.sub("(?<=^|[^\d])(\d{1,3}),?(\d{3}),?\d{3}(\.\d+)?(?=$|[^\d])",
        #                           lambda x: x.group(1) + ("." + x.group(2) if x.group(2) != "000" else "") + "M",
        #                           decontracted)
        # # Billion
        # decontracted= re.sub("(?<=^|[^\d])(\d{1,3}),?(\d{3}),?\d{3},?\d{3}(\.\d+)?(?=$|[^\d])",
        #                           lambda x: x.group(1) + ("." + x.group(2) if x.group(2) != "000" else "") + "B",
        #                           decontracted)
        decontracted=self.numbers(decontracted)
        decontracted=self.elset(decontracted)
        # replacing fractions to rationals
        #fraction with integer
        decontracted = re.sub("(\d+) (\d+)/([1-9]+)",
                               lambda x: str(round(float(format((int(x.group(1))) + float(x.group(2)) / int(x.group(3)))))) if x.group(3)!=0 else x.group(1)+' '+x.group(2)+'/'+x.group(3) ,
                               decontracted,
                               flags=re.IGNORECASE)
        #only fraction
        decontracted = re.sub("(\d+)/([1-9]+)", lambda x: str(round(float(format((int(x.group(1)) / int(x.group(2))))))) if x.group(2) !=0 else x.group(1)+'/'+x.group(2), decontracted,
                               flags=re.IGNORECASE)

        #s_frach = re.compile(r'(\d+) (\d+)/(\d+)')
        #s_frac = re.compile(r'(\d+)/(\d+)')

        #extract tokens from text
        text_tokens = keras_t.text_to_word_sequence(decontracted, filters='()*+-=:;\"`|\\<>!?“[]}{/\n//\t//,', lower=False, split=" ")
        #print("token", text_tokens)

         # text_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]
        text_tokens = [w for w in text_tokens if w.lower() not in self.stop_words]

        #handelling hashtags, numbers
        for itr, token in enumerate(text_tokens, start=0):
            # text_tokens[itr] = re.sub(r"\’", "\'", token, flags=re.IGNORECASE)
            # text_tokens[itr] = re.sub(r"\“", "\"", token, flags=re.IGNORECASE)
            # text_tokens[itr] = re.sub(r"\…", "...", token, flags=re.IGNORECASE)
            # text_tokens[itr] = re.sub(r"\”", "\"", token, flags=re.IGNORECASE)
            # text_tokens[itr] = re.sub(r"\‘", "\'", token, flags=re.IGNORECASE)
            #
            # # specific
            # text_tokens[itr] = re.sub(r"won\'t", "will not", token, flags=re.IGNORECASE)
            # text_tokens[itr] = re.sub(r"can\'t", "can not", token, flags=re.IGNORECASE)
            # text_tokens[itr] = re.sub(r"don\'t", "do not", token, flags=re.IGNORECASE)
            # text_tokens[itr] = re.sub(r"doesn\'t", "does not", token, flags=re.IGNORECASE)
            # text_tokens[itr] = re.sub(r"haven \'t", "have not", token, flags=re.IGNORECASE)
            # text_tokens[itr] = re.sub(r"(?i)i\'ve", "i have", token, flags=re.IGNORECASE)
            # text_tokens[itr] = re.sub(r"(?i)im", "i am", token, flags=re.IGNORECASE)
            #
            # # general
            # text_tokens[itr] = re.sub(r"n\'t", " not", token, flags=re.IGNORECASE)
            # text_tokens[itr] = re.sub(r"\'re", " are", token, flags=re.IGNORECASE)
            # text_tokens[itr] = re.sub(r"\'s", " is", token, flags=re.IGNORECASE)
            # text_tokens[itr] = re.sub(r"\'d", " would", token, flags=re.IGNORECASE)
            # text_tokens[itr] = re.sub(r"\'ll", " will", token, flags=re.IGNORECASE)
            # text_tokens[itr] = re.sub(r"\'t", " not", token, flags=re.IGNORECASE)
            # text_tokens[itr] = re.sub(r"\'ve", " have", token, flags=re.IGNORECASE)
            # text_tokens[itr] = re.sub(r"\'m", " am", token, flags=re.IGNORECASE)


            # remove words with 1 letter
            if (len(token) < 2 and not re.match('[0-9]',token)):
                text_tokens[itr] = ''
                continue

                # remove dots
            if (re.match('[^\d]', text_tokens[itr])):
                text_tokens[itr] = token.replace(".", '')
            #hendeling hashtags
            if (token[0] == '#'):
                text_tokens[itr] = re.sub('(#*)(#\w)', r'\2', token)
                #text_tokens.append(token.replace('#', ''))
                text_tokens.append(token.replace('#', ''))
                continue

                #token = re.sub("(\w\d.)(.+)(\w\d)", lambda x: x.group(1)+x.group(2) ,token)

                # split by upper/lower subwords
                # split by upper letter AAAbbAA
            t = re.sub("([A-Z]{2})([a-z])", r'\1 \2', token)
            f = re.sub("([a-z]{2}[0-9]*)([A-Z])", r'\1 \2', t)
            if " " in f:
                for w in f.split(" "):
                    text_tokens.append(w)
                continue


                # split word by delimiter '_'
            if '_' in token:
                for w in token.split('_'):
                    text_tokens.append(w)
                text_tokens[itr]=''
                continue

                # remove $ from words
            if (re.match(r'^\$[a-zA-Z]+|[a-zA-Z]+\$[a-zA-Z]*', token)):
                text_tokens[itr] = token.replace("$", '')
                # if (re.match('(?i)http|t.co', token)):
                #     text_tokens[itr] = ''

            if (re.match(r'&[a-zA-Z]+', token)):
                text_tokens[itr] = token.replace("&", '')



        for i in range(0,len(text_tokens),-1):
            if text_tokens[i]=='':
                del text_tokens[i]


        # text_tokens = list(filter(None, text_tokens))
        for i, ent in enumerate(entiteis, start=0):
            if (len(ent) < 2):
                entiteis[i] = ''

            # text_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]
        entiteis = [w for w in entiteis if w.lower() not in self.stop_words]
        entiteis = list(filter(None, entiteis))


        # print("final", text_tokens)

        # Stemming
        if self.stemmer:
            s = Stemmer()
            text_tokens = s.stem_term(text_tokens)
            entiteis = s.stem_term(entiteis)

        # remove_punctuation + names_and_entities + tags + hashtags + date_and_time
        return text_tokens,entiteis




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
        tokenized_text=[]
        tokenized_retweet_text=[]
        tokenized_retweet_quoted_text=[]
        tokenized_url=[]
        tokenized_retweet_url=[]
        tokenized_retweet_quoted_urls=[]
        entities=[]
        entities_retweet_1=[]
        entities_retweet_quoted_1=[]
        doc_length = 0
        max_tf = 0

        # return tuple , in place o - tokens list ,in place 1 - len of terms
        if full_text != '':
            tokenized_text, entities = self.parse_sentence(full_text)
            doc_length += len(tokenized_text)
            #s = time.process_time()

        # if retweet_text:
        #     # print(retweet_text)
        #     tokenized_retweet_text, entities_retweet_1 = self.parse_sentence(retweet_text)
        #     # print(tokenized_retweet_text)
        #
        #     doc_length += len(tokenized_retweet_text)


        # if retweet_quoted_text:
        #     tokenized_retweet_quoted_text,entities_retweet_quoted_1 = self.parse_sentence(retweet_quoted_text)
        #     doc_length += len(tokenized_retweet_quoted_text)
        #print(url)
        if url != '{}':
            tokenized_url = self.parse_url(url)
            #print(tokenized_url)
            doc_length += len(tokenized_url)
        # if retweet_url:
        #     tokenized_retweet_url = self.parse_url(retweet_url)
        #     doc_length += len(tokenized_retweet_url)
        # if retweet_quoted_urls:
        #     tokenized_retweet_quoted_urls = self.parse_url(retweet_quoted_urls)
        #     doc_length += len(tokenized_retweet_quoted_urls)

        #print("---------------------------------------------------------------------")



        # full_tokenized = tokenized_text + tokenized_retweet_text + tokenized_retweet_quoted_text
        # urls_tokenized = tokenized_url + tokenized_retweet_url + tokenized_retweet_quoted_urls
        # full_entities= entities_text_1 + entities_retweet_1 + entities_retweet_quoted_1
        #Stemming
        if self.stemmer:
            s = Stemmer()
            tokenized_text = s.stem_term(tokenized_text)

        # Stemming for urls
        if self.stemmer:
            s = Stemmer()
            tokenized_url = s.stem_term(tokenized_url)

        #print("Stemming",self.stemmer)

        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        for term in tokenized_url:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        #max_tf the max frequnce of term in doc
        if term_dict:
            max_tf = max(term_dict.values())
            nf = 1/math.sqrt(sum(pow(item,2) for item in term_dict.values()))


            #avg_veactor_toDoc(model, parsed_document)

            document = Document(tweet_id, tweet_date, full_text, url, indices, retweet_text, retweet_url,
                                retweet_indices, quote_text, quote_url, quoted_indices, retweet_quoted_text,
                                retweet_quoted_urls, retweet_quoted_indices, term_dict, doc_length ,max_tf ,nf, entities)


            return document
        else:
            return None
