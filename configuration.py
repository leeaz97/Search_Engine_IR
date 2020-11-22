class ConfigClass:
    def __init__(self):
        self.corpusPath = r'C:\Users\lazrati\Desktop\leeStudy\Data\Data\date=07-09-2020'
        self.savedFileMainFolder = r'C:\Users\lazrati\Desktop\leeStudy\Data'
        self.saveFilesWithStem = self.savedFileMainFolder + "/WithStem"
        self.saveFilesWithoutStem = self.savedFileMainFolder + "/WithoutStem"
        self.toStem = False

        print('Project was created successfully..')

    def get__corpusPath(self):
        return self.corpusPath
