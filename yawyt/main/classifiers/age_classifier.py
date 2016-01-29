import numpy
from scipy import sparse
from main.classifiers.abstract_classifier import Classifier

class AgeClassifier(Classifier):

    def __init__(self):
        Classifier.__init__(self, '/scratch2/www/yawyt3/repo/youarewhatyoutweet/yawyt/main/classifiers/aclf.joblib.pkl', '/scratch2/www/yawyt3/repo/youarewhatyoutweet/yawyt/main/classifiers/av.txt')
        self.name = 'age_classifier'

    def classify(self, tweet):
        vector = numpy.array([1 if x > 0 else 0 for x in self.vectorize(tweet.content)])
        classification = self.predict_proba(vector)
        self.add_classifications_to_tweet(tweet, {'onder20' : classification[0], '20tot40' : classification[1], '40plus' : classification[2]})
    
    def complete(self):
        pass
