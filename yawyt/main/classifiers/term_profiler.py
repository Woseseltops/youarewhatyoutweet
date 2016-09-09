import numpy
from scipy import sparse
from main.classifiers.abstract_classifier import Classifier

class TermProfiler(Classifier):

    name = 'term_profiler'
    fixed_model = False
    chosen_terms = []

    def train(self,tweets):

        for tweet in tweets:
            pass

        self.chosen_terms = ['language']

    def classify(self, tweet):

        classifications = {term: 0 for term in self.chosen_terms}

        for term in self.chosen_terms:
            if term in tweet.content:
                classifications[term] = 1

        print(classifications)

        self.add_classifications_to_tweet(tweet,classifications)
        return tweet