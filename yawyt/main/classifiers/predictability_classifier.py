from main.classifiers.abstract_classifier import Classifier

class PredictabilityClassifier(Classifier):
    
    name = 'predictability_classifier'

    def classify(self,tweet):
        self.add_classifications_to_tweet(tweet,{'predictability':0.8})