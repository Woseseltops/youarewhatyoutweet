
import codecs
import cPickle

import ucto

class Classifier():

    def __init__(self, model, vocab):

        name = ''
        with open(model, 'rb') as model_open:
            self.clf = cPickle.load(model_open)
        self.tokenizer = ucto.Tokenizer('/vol/customopt/uvt-ru/etc/ucto/tokconfig-nl-twitter')
        self.vocabulary = {}
        self.keys = []
        with codecs.open(vocab, 'r', 'utf-8') as vocabularyfile:
            self.keys = [x.strip() for x in vocabularyfile.readlines()]
        self.vocabulary_length = len(self.keys())
        self.vocabulary = {x:i for i, x in enumerate(self.keys)}

    def vectorize(self, text):

        vector = []
        self.tokenizer.process(unicode(text.decode('cp1252', 'ignore')))
        tokens = [x.text for x in self.tokenizer]
        for i, token in enumerate(tokens):
            if token[0] == '@':
                tokens[i] = 'USER'
            if re.search('^http', token):
                tokens[i] == 'URL'
        ngrams = tokens + [' '.join(x) for x in zip(tokens_n, tokens_n[1:]) ] + [ '_'.join(x) for x in zip(tokens_n, tokens_n[1:], tokens_n[2:])]
        in_vocabulary = [(x, ngrams.count(x)) for x in list(set(ngrams) - set(self.keys))]
        vector = [0.0] * self.vocabulary_length
        for ngram in in_vocabulary:
            vector[self.vocabulary[ngram[0]]] = ngram[1] 
        return vector

    def classify(self, vector):

        classification = self.clf.predict(vector)
        proba = self.clf.predict_proba(vector)
        return classification, proba.tolist()

    def add_classifications_to_tweet(self, tweet, classifications):
        tweet.automatic_classifications[self.name] = classifications