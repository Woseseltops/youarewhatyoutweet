from main.classifiers.abstract_classifier import Classifier
from soothsayer.predictability import get_predictability_for_sentence
from yawyt.settings import SOOTHSAYER_SERVER_URL

class PredictabilityClassifier(Classifier):
    
    name = 'predictability_classifier'

    def classify(self,tweet):
#        predictability = get_predictability_for_sentence(tweet.content,SOOTHSAYER_SERVER_URL)
        predictability = 0.4
        print(predictability)
        self.add_classifications_to_tweet(tweet,{'predictability':predictability})