class ReleventDocData:

    def __init__(self,id=0,terms=[],idf=0,tf_normal=0,date=''):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.num_id = id
        self.terms= []
        #self.idf = idf
        #self.tf_normal = tf_normal
        #self.date = date