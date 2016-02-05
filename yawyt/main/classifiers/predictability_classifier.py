from main.classifiers.abstract_classifier import Classifier
from soothsayer.predictability import get_predictability_for_sentence

class PredictabilityClassifier(Classifier):
    
    name = 'predictability_classifier'

    def classify(self,tweet):
        self.add_classifications_to_tweet(tweet,{'predictability':0.8})