import pickle
import re
import ucto
from main.classifiers.abstract_classifier import Classifier

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

class SklearnClassifier(Classifier):

    def __init__(self, model, vocab):

        name = ''
        with open(model, 'rb') as model_open:
            self.clf = pickle.load(model_open)
#        self.tokenizer = ucto.Tokenizer('/vol/customopt/lamachine/etc/ucto/tokconfig-nl')
        self.vocabulary = {}
        self.keys = []
        with open(vocab, 'r', encoding = 'utf-8') as vocabularyfile:
            self.keys = [x.strip() for x in vocabularyfile.readlines()]
        self.vocabulary_length = len(self.keys)
        self.vocabulary = {x:i for i, x in enumerate(self.keys)}

    def vectorize(self, text, underscore=False, user=False, url=False):

        tokenizer = ucto.Tokenizer('/vol/customopt/lamachine/etc/ucto/tokconfig-nl-twitter')
        text = text[2:-1]
        vector = []
        if underscore:
            text = '<s> ' + text + ' <s>'
        tokens = []
        tokenizer.process(text)
        for token in tokenizer:
            if not token.tokentype == 'PUNCTUATION':
                if user and token.text[0] == '@':
                    tokens.append('USER')
                elif url and re.search('^http', token):
                    tokens.append('URL')
                else:
                    tokens.append(token.text)
        if underscore:
            ngrams = tokens + ['_'.join(x) for x in zip(tokens, tokens[1:]) ] + [ ' '.join(x) for x in zip(tokens, tokens[1:], tokens[2:])]
        else:
            ngrams = tokens + [' '.join(x) for x in zip(tokens, tokens[1:]) ] + [ ' '.join(x) for x in zip(tokens, tokens[1:], tokens[2:])]
        in_vocabulary = [(x, float(ngrams.count(x))) for x in list(set(ngrams) & set(self.keys))]
        #print('IN VOCABULARY', in_vocabulary)
        vector = [0.0] * self.vocabulary_length
        for ngram in in_vocabulary:
            vector[self.vocabulary[ngram[0]]] = ngram[1] 
        return vector

    def predict_proba(self, vector):
        
        predict = self.clf.predict(vector)
        proba = self.clf.predict_proba(vector)
        return proba.tolist()[0]
