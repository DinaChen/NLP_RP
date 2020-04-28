import dataProcess
import spacy
sp = spacy.load('en_core_web_sm')
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import csv
import string
from gensim.models import Phrases
from gensim.models import Word2Vec

from nltk.stem import LancasterStemmer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

#One can generate its own set of rules for any language that is
# why Python nltk introduced SnowballStemmers that are used to create non-English Stemmers!

# First tokenize, then remove punctuation and stop words.
# lemmatization before tokenization?
def main():

    bigram = Phrases()
    lancaster = LancasterStemmer()
    porter = PorterStemmer()

    file = 'transcripts/season1/0101.html'
    friends0101 = dataProcess.episodeTranscript(file)
    #dataProcess.printLines(friends0101)
    #print(len(friends0101))


    bags = []
    for sentence in friends0101:
        wordBag = nltk.word_tokenize(sentence)
        wordBag_puncFree = []
        for word in wordBag:
            if word not in string.punctuation and word not in stopwords.words("english"): # && not "..."
                #wordBag_puncFree.append(porter.stem(word))   # stem?
                wordBag_puncFree.append(word)
                bigram.add_vocab([wordBag_puncFree])
        bags.append(wordBag_puncFree)

    dataProcess.printLines(bags)  ##
    print(len(friends0101))
    print(len(bags))

    bigram.add_vocab([bags])
    bigram_model = Word2Vec(bigram[bags], size=100)
    print(bigram_model.similarity("date", "new"))


def tokenize():
    sample = "Ahh, miss? c'mon  More coffee? Ugh.  Excuse me, could you give this to that guy over there?  " \
             "Go ahead.  Thank you. why?! Sorry. Okay, Las Vegas. Okay, so, I'm in Las Vegas... oh...see..."

    print(nltk.word_tokenize(sample))

def stem():

    print(lancaster.stem("you're"))
    print(lancaster.stem("you are"))
    print(lancaster.stem("'re"))

def spacy():
    sentence = sp(u'Manchester United is looking to sign a forward for $90 million')
    print(sentence)
    porter = PorterStemmer()

    for word in sentence:
        print(word)
        print(word.pos_)

        if (word.pos_ == 'VERB'):
            print('hi')
            st = porter.stem(word)  # only used by string
            print(st)


main()
#tokenize()
#spacy()