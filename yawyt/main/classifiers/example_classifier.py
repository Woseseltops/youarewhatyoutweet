from abstract_classifier import Classifier

class ExampleClassifier(Classifier):
    
    name = 'example'

    def classify(self,tweet):
    	
        #Tokenize
        tokens = tweet.content.split()

        if 'rood' in tokens:
            self.add_classifications_to_tweet(tweet,{'rood':1,'bruin':0,'blond':0})
        else:
            self.add_classifications_to_tweet(tweet,{'rood':0.3,'bruin':0.3,'blond':0.3})

#You can play with a classifier as standalone like this
if __name__ == '__main__':
	
    from main.twitter.tweet import Tweet	

    tweets_to_classify = [Tweet(1,'wessel','ik heb blond haar'),
                          Tweet(2,'bassie','ik heb rood haar')]

    classifier = ExampleClassifier()
    
    for tweet in tweets_to_classify:
        classifier.classify(tweet);
        print(tweet.automatic_classifications);
