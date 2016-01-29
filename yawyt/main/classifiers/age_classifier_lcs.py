from main.classifiers.abstract_lcs_classifier import LcsClassifier
from main.twitterlib import tweet

class AgeClassifier(LcsClassifier):

    def __init__(self):
        LcsClassifier.__init__(self)
        self.model = '/scratch2/www/yawyt3/repo/youarewhatyoutweet/yawyt/main/classifiers/age_data/'
        self.name = 'age_classifier_lcs'

    def classify(self, tweet):        
        self.make_file(tweet)
        
    def complete(self):
        classifications = self.predict(self.model)
        for classification in classifications:
            print(classification[1])
            self.add_classifications_to_tweet(classification[0], {'onder20' : classification[1]['0'], '20tot40' : classification[1]['1'], '40plus' : classification[1]['2']})

if __name__ == '__main__':

    ttweet1 = tweet.Tweet(1, 'pietje', 'ik ben een harige oude man van 40')
    ttweet2 = tweet.Tweet(2, 'jay', 'al die homeboys kunnen me djoeken g')

    ac = AgeClassifier()
    ac.classify(ttweet1)
    ac.classify(ttweet2)
    
