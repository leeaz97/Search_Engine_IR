import numpy as np

class ReleventDocData:

    def __init__(self,id=0,terms=[],idf=0,date='',nf=0,vec_doc= np.zeros(300, ),tf_normal=0,):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.num_id = id
        self.terms = terms
        self.nf = nf
        self.idf = idf
        self.date =date
        self.vec_doc = vec_doc
        #self.tf_normal = tf_normal
        #self.date = date