from sklearn.externals import joblib
import codecs
import numpy

from abstract_classifier import Classifier

class GenderClassifier(Classifier):

    def __init__(self, model, vocab):

        Classifier.__init__(self, model, vocab)
        #with codecs.open(weights, 'r', 'utf-8') as weights_file:
        #    self.weights = numpy.array([float(x.strip()) for x in weights_file.readlines()])
        self.name = 'age_classifier'

    def classify(self, tweet):

        if tweet.content[:2] != "RT":
            #vector = numpy.array(self.vectorize(tweet.content)) * self.weights
            vector = self.vectorize(tweet.content)
            classification = self.predict(vector)
            try:
                print(tweet.content)
            except:
                print('decode error')
            self.add_classifications_to_tweet(tweet, {'onder 20' : classification[0], '20-40' : classification[1], '40 plus' : classification[2]})

#You can play with a classifier as standalone like this
if __name__ == '__main__':

    #Set the python path to contain our library with twitter specific code
    import sys
    import os
    sys.path.append(os.path.abspath(__file__ + '/../../'))

    #Import that twitter specific code
    from twitterlib.tweet import Tweet

    #The actual code
    tweets_to_classify = [Tweet(1, 'wessel', '@OHMYTESSA gefeliciteerd ::)'),
        Tweet(2, 'd', '@jordybremer maak er een foto van'),
        Tweet(3, 'e', '@Pascal_12321  ik 5.8 ha'),
        Tweet(4, 'f', '@celineruttenx oo bedankt'),
        Tweet(5, 'g', 'RT @XxxFroukje: @celineruttenx @jessywissingx @NiekvanBon @lol_sem_lol yeahh!!!'),
        Tweet(6, 'h', '"@voetbalyeah: Want zij gelooft in mij zij ziet toekomst in ons allebei" jordy waarom heet je nie gewoon  raadhetliedje'),
        Tweet(7, 'i', '"@Ik_ben_Valo: Hallo" doei'),
        Tweet(8, 'j', '"@AgnesXvoetbal: Nu tosti eten x" ik wil ook tosti'),
        Tweet(9, 'k', 'RT @KutSteen: Jij bent zo dik dat als je met een gele jas een berg op loopt ik denk dat de zon op komt.'),
        Tweet(10, 'l', '"@Thelco28: "@EefOnstenk: hee dikke waar ben je ? @WinHeskes � ze is facking hard op dr bek gegaan, ennu kan ze niet meer fietsen." Lol'),
        Tweet(11, 'm', '"@olivierhaker: Omw to oma in alkmaar erna naar ajax psv in skybox arena :D" vet'),
        Tweet(12, 'n', 'Ik #staop voor @olivierhaker  en veerle'),
        Tweet(13, 'o', '@AgnesXvoetbal  nmmr ???'),
        Tweet(15, 'p', '@shirleyxpeters  likt @xfleurbuurman en brit anaalt'),
        Tweet(16, 'q', 'Sick'),
        Tweet(17, 'r', 'Je tanden zijn mooi kaja, heb je een vals gebit ? - opavoice �'),
        Tweet(18, 's', '@aishasw_a imess x'),
        Tweet(19, 't', 'Nooit gedachtdat me kamer zo opgeruimt zou zijn o'),
        Tweet(20, 'u', '@AlyssaLOVE_ jaatoch ;D'),
        Tweet(21, 'v', 'Ik voel me snel aangesproken, ja'),
        Tweet(22, 'w', 'Mygod morgen 23 graden in nl �')
        ]
        
    classifier = GenderClassifier('/vol/tensusers/fkunneman/exp/profl/exp_gender/token_ngrams_frequency_7500/nb/fold_7/classifiermodel.joblib.pkl', 
        '/vol/tensusers/fkunneman/exp/profl/exp_gender/token_ngrams_frequency_7500/nb/fold_7/vocabulary.txt')
    
    for tweet in tweets_to_classify:
        classifier.classify(tweet)
        print(tweet.automatic_classifications)