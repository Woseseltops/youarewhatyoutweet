import numpy
from main.classifiers.abstract_sklearn_classifier import SklearnClassifier

class GenderClassifier(SklearnClassifier):

    name = 'gender_classifier'

    def __init__(self):

        SklearnClassifier.__init__(self, '/scratch2/www/yawyt3/repo/youarewhatyoutweet/yawyt/main/classifiers/gclf.joblib.pkl', '/scratch2/www/yawyt3/repo/youarewhatyoutweet/yawyt/main/classifiers/gv.txt')
#        with open('/scratch2/www/yawyt3/repo/youarewhatyoutweet/yawyt/main/classifiers/gw.txt') as weights_file:
 #           self.weights = [float(x.strip()) for x in weights_file.readlines()]
        self.name = 'gender_classifier'

    def classify(self, tweet):
        if tweet.content[2:5] != "RT ":
            vector = numpy.array([1 if x > 0 else 0 for x in self.vectorize(tweet.content)])
            #vector = numpy.array(self.vectorize(tweet.content)) * numpy.array(self.weights)
            classification = self.predict_proba(vector)
            self.add_classifications_to_tweet(tweet, {'man' : classification[1], 'vrouw': classification[0]})
        return tweet

	
