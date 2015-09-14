from sklearn.externals import joblib
import codecs
import numpy

class GenderClassifier(Classifier):

    def __init__(self, model, vocab, weights):

        Classifier.__init__(self, model, vocab)
        with codecs.open(weights, 'r', 'utf-8') as weights_file:
            self.weights = numpy.array([float(x.strip()) for x in weights_file.readlines()]):
        name = 'gender_classifier'

    def classify(self, tweet):
        
        if tweet.text[:2] != "RT":
            vector = numpy.array(self.vectorize(tweet.text)) * self.weights
            classification = self.classify(vector)
            print(classification)
            quit()
            self.add_classifications_to_tweet(tweet, {'man': 0, 'vrouw': 1})

#You can play with a classifier as standalone like this
if __name__ == '__main__':

    #Set the python path to contain our library with twitter specific code
    import sys
    import os
    sys.path.append(os.path.abspath(__file__ + '/../../'))

    #Import that twitter specific code
    from twitterlib.tweet import Tweet

    #The actual code
    tweets_to_classify = [Tweet(1, 'wessel', 'ik heb blond haar'),
                          Tweet(2, 'bassie', 'ik heb rood haar')]

    classifier = GenderClassifier()
    
    for tweet in tweets_to_classify:
        classifier.classify(tweet)
        print(tweet.automatic_classifications)
