import pickle
from gensim.models import KeyedVectors


def load_GoogleNews_vectors_negative300(filename):
    # load the google word2vec model
    model = KeyedVectors.load_word2vec_format(filename, binary=True)
    return model

def save_obj(obj, name):
    """
    This function save an object as a pickle.
    :param obj: object to save
    :param name: name of the pickle file.
    :return: -
    """
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    with open(name + '.txt', 'w',encoding="utf-8") as f:
        f.write(str(obj))
        f.closed
        #pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    """
    This function will load a pickle file
    :param name: name of the pickle file
    :return: loaded pickle file
    """
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
