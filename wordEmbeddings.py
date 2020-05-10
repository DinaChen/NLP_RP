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
from gensim.models import KeyedVectors
from gensim.test.utils import get_tmpfile

from nltk.stem import LancasterStemmer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

#One can generate its own set of rules for any language that is
# why Python nltk introduced SnowballStemmers that are used to create non-English Stemmers!

# First tokenize, then remove punctuation and stop words.
# lemmatization before tokenization?
def main():

    phr = Phrases()
    lancaster = LancasterStemmer()
    porter = PorterStemmer()

    file = 'transcripts/season1/0101.html'
    f0101 = dataProcess.episodeTranscript(file)

    #dataProcess.printLines(f0101)

    bags = []
    for sentence in f0101:
        wordBag = nltk.word_tokenize(sentence)
        wordBag_puncFree = []
        for word in wordBag:
            if word not in string.punctuation and word not in stopwords.words("english"): # && not "..."
                #wordBag_puncFree.append(porter.stem(word))   # stem?
                wordBag_puncFree.append(word)
                phr.add_vocab([wordBag_puncFree])
        bags.append(wordBag_puncFree)

    dataProcess.printLines(list(phr[bags]))
    print(len(f0101))
    print(len(bags))

    #phr.add_vocab([bags])
    friendsW2v = Word2Vec(phr[bags], min_count=1, size=32)

    word_vectors = friendsW2v.wv
    fname = get_tmpfile("vectors.kv")
    word_vectors.save(fname)
    word_vectors = KeyedVectors.load(fname, mmap='r')

    vec = word_vectors.get_vector('work')
    print(vec)

    #odel = Word2Vec(common_texts, size=100, window=5, min_count=1, workers=4)   window?
    #print(friendsW2v.similarity("look", "dream"))
    #print(friendsW2v.wv['look'])
    #print(friendsW2v.get_vector('just'))









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