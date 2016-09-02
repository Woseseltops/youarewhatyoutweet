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

        self.chosen_terms = ['voetbal','koken','Game_of_Thrones']

    def classify(self, tweet):

        self.add_classifications_to_tweet(tweet,{term: 1 for term in self.chosen_terms})
        return tweet