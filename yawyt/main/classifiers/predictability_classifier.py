from main.classifiers.abstract_classifier import Classifier
from yawyt.settings import SOOTHSAYER_BASE_LOCATION, SOOTHSAYER_MODEL_LOCATION
from soothsayer.predictability import get_predictability_for_sentence

class PredictabilityClassifier(Classifier):
    
    name = 'predictability_classifier'

    def classify(self,tweet):
        predictability = get_predictability_for_sentence(tweet.content,SOOTHSAYER_BASE_LOCATION,SOOTHSAYER_MODEL_LOCATION)
        self.add_classifications_to_tweet(tweet,{'predictability':predictability})
        return tweet
