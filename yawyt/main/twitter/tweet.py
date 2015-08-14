PACKAGE_ORDER = ['id','author','content']

class Tweet():

    def __init__(self,id,author,content):
        self.id = id
        self.author = author
        self.content = content
        self.automatic_classifications = {}

    def package(self):

        return '\t'.join([str(getattr(self,propertyname)) for propertyname in PACKAGE_ORDER])

def tweet_list_to_files_per_author(tweetlist,folderpath):

    files = {}

    for tweet in tweetlist:

        if tweet.author not in files.keys():
            files[tweet.author] = open(folderpath+tweet.author+'.txt','w')

        files[tweet.author].write(tweet.package()+'\n')

def tweet_annotations_to_files_per_author(tweetlist,folderpath):

    files = {}

    for tweet in tweetlist:

        if tweet.author not in files.keys():
            files[tweet.author] = {}
            for classification in tweet.automatic_classifications.keys():
                files[tweet.author][classification] = open(folderpath+tweet.author+'.'+classification+'.txt','w')

        for classification, score in tweet.automatic_classifications.items():
            files[tweet.author][classification].write(tweet.id+'\t'+score+'\n')

def file_to_tweet_list(filepath):

    tweetlist = []

    for line in open(filepath):
        current_tweet = Tweet(0,'','')

        #Load every item on the line, using the package_order
        [setattr(current_tweet,PACKAGE_ORDER[n],item) for n, item in enumerate(line.split())]

        tweetlist.append(current_tweet)

    return tweetlist

if __name__ == '__main__':

    t = Tweet(1,'wessel','hoi')
    print(t.package())