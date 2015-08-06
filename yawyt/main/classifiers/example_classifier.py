from abstract_classifier import Classifier

class ExampleClassifier(Classifier):
    
    name = 'example'

    def classify(self,tweet):
    	
        if 'ik heb rood haar' in tweet.content:
            self.add_classification_to_tweet({'rood':1,'bruin':0,'blond':0})

        else:
            self.add_classification_to_tweet({'rood':0.3,'bruin':0.3,'blond':0.3})
