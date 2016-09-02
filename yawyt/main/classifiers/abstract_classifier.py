class Classifier():

    name = ''
    fixed_model = True #if set to false, will call the train method first

    def add_classifications_to_tweet(self,tweet,classifications):
        tweet.automatic_classifications[self.name] = classifications

    def classify(self,tweet):

        raise NotImplementedError

    def train(self,tweets):

        raise NotImplementedError

    def complete(self):
        pass