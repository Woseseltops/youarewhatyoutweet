import numpy
from main.classifiers.abstract_sklearn_classifier import SklearnClassifier

class SarcasmeClassifier(SklearnClassifier):

    def __init__(self):

        SklearnClassifier.__init__(self, '/scratch2/www/yawyt3/repo/youarewhatyoutweet/yawyt/main/classifiers/sarclf.joblib.pkl', '/scratch2/www/yawyt3/repo/youarewhatyoutweet/yawyt/main/classifiers/sarv.txt')
#        with open('/scratch2/www/yawyt3/repo/youarewhatyoutweet/yawyt/main/classifiers/sw1.txt') as weights_file:
#            self.weights = numpy.array([float(x.strip()) for x in weights_file.readlines()])
        self.name = 'sarcasm_classifier'

    def classify(self, tweet):
        if tweet.content[2:5] != "RT ":
#            vector = numpy.array(self.vectorize(tweet.content.lower())) * self.weights
            vector = numpy.array([1 if x > 0 else 0 for x in self.vectorize(tweet.content)])
            classification = self.predict_proba(vector)
            self.add_classifications_to_tweet(tweet, {'sarcastic' : classification[1]})
        return tweet
