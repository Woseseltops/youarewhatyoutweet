import numpy
from scipy import sparse
from main.classifiers.abstract_classifier import Classifier
from yawyt.settings import BASE_DIR
import pickle
import re
import math
from operator import itemgetter

class TermProfiler(Classifier):

    name = 'term_profiler'
    fixed_model = False
    chosen_terms = []
    NUMBER_OF_TERMS = 3
    DATA_DIR = BASE_DIR+'main/classifiers/term_profiler_data/'

    def train(self,tweets):

        #Read background file
        with open(self.DATA_DIR+'nlsave.pickle', 'rb') as handle:
            bg_dict, bg_term_count = pickle.load(handle)

        #Process the tweets
        fg_dict, fg_term_count = self.read_text_in_dict('%boundary%'.join([tweet.content for tweet in tweets]))

        #Real calculations start here
        kldiv_per_term = dict()

        for term in fg_dict:
            fg_freq = fg_dict[term]

            # kldivI is kldiv for informativeness: relative to bg corpus freqs
            bg_freq = 1
            if term in bg_dict:
                bg_freq = bg_dict[term]
            relfreq_fg = float(fg_freq) / float(fg_term_count)
            relfreq_bg = float(bg_freq) / float(bg_term_count)

            kldivI = relfreq_fg * math.log(relfreq_fg / relfreq_bg)

            # kldivP is kldiv for phraseness: relative to unigram freqs
            unigrams = term.split(" ")
            relfreq_unigrams = 1.0
            for unigram in unigrams:
                if unigram in fg_dict:
                    # stopwords are not in the dict
                    u_freq = fg_dict[unigram]
                    u_relfreq = float(u_freq) / float(fg_term_count)
                    relfreq_unigrams *= u_relfreq
            kldivP = relfreq_fg * math.log(relfreq_fg / relfreq_unigrams)
            kldiv = kldivI + kldivP
            kldiv_per_term[term] = kldiv

        ordered_terms = [term for term,score in sorted(kldiv_per_term.items(),key=itemgetter(1),reverse=True)]
        self.chosen_terms = ordered_terms[:self.NUMBER_OF_TERMS]

    def classify(self, tweet):

        classifications = {term: 0 for term in self.chosen_terms}

        for term in self.chosen_terms:
            if term.lower() in tweet.content.lower().replace('_',''):
                classifications[term] = 1

        self.add_classifications_to_tweet(tweet,classifications)
        return tweet

    def read_text_in_dict(self,text):
        freq_dict = self.get_all_ngrams(text,3)
        total_term_count = 0
        for key in freq_dict:
            total_term_count += freq_dict[key]
        return freq_dict, total_term_count


    def get_all_ngrams(self,text, maxn):
        stoplist = [word.strip() for word in open(self.DATA_DIR+'stoplist.txt')]

        words = self.tokenize(text)
        i = 0
        terms = dict()

        for n, word in enumerate(words):

            if n % 10000 == 0:
                print(n / len(words))

            if word not in stoplist and len(word) > 1 and '@' not in word:
                if word in terms:
                    terms[word] += 1
                else:
                    terms[word] = 1
            if maxn >= 2:
                if i < len(words) - 1:
                    if words[i] not in stoplist and words[i + 1] not in stoplist:
                        bigram = words[i] + " " + words[i + 1]
                        if bigram in terms:
                            terms[bigram] += 1
                        else:
                            terms[bigram] = 1

                    if maxn >= 3:
                        if i < len(words) - 2:
                            if not words[i] in stoplist and not words[i + 2] in stoplist:
                                # middle word can be a stopword
                                trigram = words[i] + " " + words[i + 1] + " " + words[i + 2]
                                if trigram in terms:
                                    terms[trigram] += 1
                                else:
                                    terms[trigram] = 1
            i += 1
        return terms

    def tokenize(self,t):
        text = t.lower()
        text = re.sub("\n", " ", text)
        text = re.sub(r'<[^>]+>', "", text)  # remove all html markup
        text = re.sub('[^a-zèéeêëûüùôöòóœøîïíàáâäæãå&@#A-Z0-9- \']', "", text)
        wrds = text.split()
        return wrds

