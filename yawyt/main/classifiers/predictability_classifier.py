from main.classifiers.abstract_classifier import Classifier
from soothsayer.predictability import get_predictability_for_sentence

class PredictabilityClassifier(Classifier):
    
    name = 'predictability_classifier'

    def classify(self,tweet):
        predictability = get_predictability_for_sentence(tweet.content)
        print('predictability',predictability)
        self.add_classifications_to_tweet(tweet,{'predictability':predictability})