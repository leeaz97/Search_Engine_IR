import numpy as np
class Document:

    def __init__(self, tweet_id, tweet_date=None, full_text=None, url=None, indices=None, retweet_text=None, retweet_url=None,
                 retweet_indices=None, quote_text=None, quote_url=None, quoted_indices=None, retweet_quoted_text=None,
                 retweet_quoted_urls=None, retweet_quoted_indices=None, term_doc_dictionary=None, doc_length=0 ,max_tf=0,nf=0,entities=[]):#,v_doc=np.zeros(300, )): #,tf_normal=0):
        """
        :param tweet_id: tweet id
        :param tweet_date: tweet date
        :param full_text: full text as string from tweet
        :param url: url
        :param retweet_text: retweet text
        :param retweet_url: retweet url
        :param quote_text: quote text
        :param quote_url: quote url
        :param term_doc_dictionary: dictionary of term and documents.
        :param doc_length: doc length
        """
        self.tweet_id = tweet_id
        self.tweet_date = tweet_date
        self.full_text = full_text
        self.url = url
        self.retweet_text = retweet_text
        self.retweet_url = retweet_url
        self.quote_text = quote_text
        self.quote_url = quote_url
        self.term_doc_dictionary = term_doc_dictionary
        self.doc_length = doc_length
        self.indices = indices
        self.retweet_indices = retweet_indices
        self.quoted_indices = quoted_indices
        self.retweet_quoted_text = retweet_quoted_text
        self.retweet_quoted_urls = retweet_quoted_urls
        self.retweet_quoted_indices = retweet_quoted_indices
        self.max_tf = max_tf
        self.nf = nf
        self.entities = entities


