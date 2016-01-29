
import os
import re
import ucto

class LcsClassifier():

    def __init__(self):

        name = ''
        os.chdir('/scratch2/www/yawyt3/repo/youarewhatyoutweet/yawyt/main/classifiers/')
        os.mkdir('files/')
        self.tokenizer = ucto.Tokenizer('/vol/customopt/lamachine/etc/ucto/tokconfig-nl-twitter')
        self.f = 0
        self.tweets = []

    def make_file(self, tweet):
        self.tweets.append(tweet)
        # prepare files
        fd = 'files/'
        fn = 'f' + str(self.f) + '.txt'
        self.f += 1
        test = 'test'
        # featurize
        text = tweet.content[2:-1]
        self.tokenizer.process(text)
        tokens = [x.text for x in self.tokenizer]
        ngrams = tokens + [' '.join(x) for x in zip(tokens, tokens[1:]) ] + [ ' '.join(x) for x in zip(tokens, tokens[1:], tokens[2:])]
        # write files
        with open(fd + fn, 'w', encoding = 'utf-8') as outfile: 
            outfile.write('\n'.join(ngrams))
        with open(test, 'a', encoding = 'utf-8') as tf:
            tf.write(fn + '\n')

    def predict(self, cldir):
        os.system('/vol/customopt/machine-learning/lib/lcs3.8/production.jar ' + cldir + ' /scratch2/www/yawyt3/repo/youarewhatyoutweet/yawyt/main/classifiers/test > /scratch2/www/yawyt3/repo/youarewhatyoutweet/yawyt/main/classifiers/classification.txt')
        os.system('rm -r /scratch2/www/yawyt3/repo/youarewhatyoutweet/yawyt/main/classifiers/files/')
        os.system('rm /scratch2/www/yawyt3/repo/youarewhatyoutweet/yawyt/main/classifiers/test')
        os.chdir('/scratch2/www/yawyt3/repo/youarewhatyoutweet/yawyt/')
        with open('/scratch2/www/yawyt3/repo/youarewhatyoutweet/yawyt/main/classifiers/classification.txt', encoding = 'utf-8') as infile:
            results = infile.read().strip().split('\n')
        output = []
        for i, result in enumerate(results):
            tokens = result.split()
            scores = list(set(tokens[1:]))
            classification = {}
            for score in scores:
                t = score.split(':')
                c = re.sub('\?', '', t[0])
                s = float(t[1]) / 15
                if s > 1:
                    s = 1.0
                elif s < 0:
                    s = 0.0
                classification[c] = s            
            output.append((self.tweets[i], classification))
        return output
                
    def add_classifications_to_tweet(self, tweet, classifications):
        tweet.automatic_classifications[self.name] = classifications
