import os

class ConfigClass:
    def __init__(self,corpus_path='',output_path='',stemming=False):
        self.corpusPath = corpus_path
        self.savedFileMainFolder = output_path
        self.saveFilesWithStem = os.path.join(self.savedFileMainFolder,"WithStem")
        self.saveFilesWithoutStem = os.path.join(self.savedFileMainFolder,"WithoutStem")
        self.toStem = stemming
        self.number_of_documents = 0


        print('Project was created successfully..')

    def get__corpusPath(self):
        return self.corpusPath

    def get__outputPath(self):
        if self.toStem:
            return self.saveFilesWithStem
        else:
            return self.saveFilesWithoutStem

    #def get__word2vecPath(self):
    #    return self.corpusPath
