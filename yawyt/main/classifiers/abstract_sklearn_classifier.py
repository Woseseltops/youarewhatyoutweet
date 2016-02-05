import pickle
import re
import ucto
from main.classifiers.abstract_classifier import Classifier

class SklearnClassifier(Classifier):

    def __init__(self, model, vocab):

        name = ''
        with open(model, 'rb') as model_open:
            self.clf = pickle.load(model_open)
        self.tokenizer = ucto.Tokenizer('/vol/customopt/lamachine/etc/ucto/tokconfig-nl-twitter')
        self.vocabulary = {}
        self.keys = []
        with open(vocab, 'r', encoding = 'utf-8') as vocabularyfile:
            self.keys = [x.strip() for x in vocabularyfile.readlines()]
        self.vocabulary_length = len(self.keys)
        self.vocabulary = {x:i for i, x in enumerate(self.keys)}

    def vectorize(self, text, underscore = False):

        text = text[2:-1]
        vector = []
        if underscore:
            text = '<s> ' + text + ' <s>'
            self.tokenizer.process(text)
            tokens = [x.text for x in self.tokenizer]
            for i, token in enumerate(tokens):
                if token[0] == '@':
                    tokens[i] = 'USER'
                if re.search('^http', token):
                    tokens[i] == 'URL'
            ngrams = tokens + ['_'.join(x) for x in zip(tokens, tokens[1:]) ] + [ ' '.join(x) for x in zip(tokens, tokens[1:], tokens[2:])]
        else:
            self.tokenizer.process(text)
            tokens = [x.text for x in self.tokenizer]          
            ngrams = tokens + [' '.join(x) for x in zip(tokens, tokens[1:]) ] + [ ' '.join(x) for x in zip(tokens, tokens[1:], tokens[2:])]
        in_vocabulary = [(x, float(ngrams.count(x))) for x in list(set(ngrams) & set(self.keys))]
        vector = [0.0] * self.vocabulary_length
        for ngram in in_vocabulary:
            vector[self.vocabulary[ngram[0]]] = ngram[1] 
        return vector

    def predict_proba(self, vector):
        
        predict = self.clf.predict(vector)
        proba = self.clf.predict_proba(vector)
        return proba.tolist()[0]
