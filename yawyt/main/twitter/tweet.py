class Tweet():

    def __init__(self,id,author,content):
        self.id = id
        self.author = author
        self.content = content
        self.automatic_classifications = {}
