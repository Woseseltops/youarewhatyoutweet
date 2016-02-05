class Classifier():

    name = ''

    def add_classifications_to_tweet(self,tweet,classifications):
        tweet.automatic_classifications[self.name] = classifications

    def classify(self,tweet):

        raise NotImplementedError

    def complete(self):
        pass