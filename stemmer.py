from nltk.stem import snowball
from nltk.stem.snowball import SnowballStemmer

class Stemmer:
    def __init__(self):
        #self.stemmer = snowball.SnowballStemmer("english")
        self.stemmer = SnowballStemmer(language='english')

    def stem_term(self, tokens):
        """
        This function stem a token
        :param token: string of a token
        :return: stemmed token
        """
        list_after_stemming = []
        t = ""
        for token in tokens:
            #print(type(token),token)
            stem_token = self.stemmer.stem(token)
            # if not do stemming save the token as is
            if stem_token == token.lower():
                list_after_stemming.append(token)
            else:
                # if the token was Uppercase, save him after stemming as Uppercase
                if token.isupper():
                    list_after_stemming.append(stem_token.upper())
                # if the token was Lowercase, save him after stemming as Lowercase
                elif token.islower():
                    list_after_stemming.append(stem_token)

                    # elif token[0].isupper():
                    # list_after_stemming.append(stem_token[0].upper() + stem_token[1:])
                # if the token contain Uppercase and lowercase , save him as its was
                else:
                    for i in range(len(stem_token)):
                        if token[i].isupper():
                            t += stem_token[i].upper()
                        else:
                            t += stem_token[i]
                    list_after_stemming.append(t)
                    t = ""

        return list_after_stemming

        #return self.stemmer.stem(token)
