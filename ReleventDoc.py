import numpy as np

class ReleventDocData:

    def __init__(self,num=0,terms=[],nf=0,date='',vec_doc= np.zeros(300, )):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.num_show = num
        self.terms = terms
        self.nf = nf
        self.date =date
        self.vec_doc = vec_doc
