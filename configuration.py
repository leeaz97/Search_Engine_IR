import os

class ConfigClass:
    def __init__(self):
        self.corpusPath = r'C:\Users\lazrati\Desktop\leeStudy\Data\Data\date=07-09-2020'
        self.savedFileMainFolder = r'C:\Users\lazrati\Desktop\leeStudy\Data'
        self.saveFilesWithStem = os.path.join(self.savedFileMainFolder,"WithStem")
        self.saveFilesWithoutStem = os.path.join(self.savedFileMainFolder,"WithoutStem")
        self.toStem = False
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
