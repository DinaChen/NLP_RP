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
from gensim.test.utils import datapath
from gensim.test.utils import get_tmpfile
import random
import math
from nltk.stem import LancasterStemmer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import gensim.downloader as api
import numpy as np


#One can generate its own set of rules for any language that is
# why Python nltk introduced SnowballStemmers that are used to create non-English Stemmers!
# First tokenize, then remove punctuation and stop words.
# lemmatization before tokenization?

def main():

    friends_data = dataProcess.friends()
    tbbt_data = dataProcess.bigbang()
    himym_data = dataProcess.himym()


    # Get KeyedVectors of word2Vec embeddings, only tokenization and punctuation removal.
    friends = KeyedVectors.load(get_tmpfile('friends.bin'), mmap='r')
    tbbt = KeyedVectors.load(get_tmpfile('tbbt.bin'), mmap='r')
    himym = KeyedVectors.load(get_tmpfile('himym.bin'), mmap='r')

    # Get normalizing factor (add up all the words in the vocabulary together)
    t_Nfactor = getNormFactor(tbbt)
    f_Nfactor = getNormFactor(friends)
    h_Nfactor = getNormFactor(himym)

    (trainDataF, testDataF) = cutList(friends_data, 0.8)
    (trainDataT, testDataT) = cutList(tbbt_data, 0.8)
    (trainDataH, testDataH) = cutList(himym_data, 0.8)
    #lancaster = LancasterStemmer()
    #porter = PorterStemmer()
    #generateW2V(trainDataF, trainDataT, trainDataH)
    #friend = KeyedVectors.load_word2vec_format('w2v/friends.bin', binary=True, encoding= 'unicode_escape')

    (t1, t2) = cutList(testDataT, 0.3)
    (h1, h2) = cutList(testDataH, 0.3)
    (f1, f2) = cutList(testDataF, 0.3)

    #test(testDataF, f_Nfactor, t_Nfactor, h_Nfactor, friends, tbbt, himym)
    #test(testDataT, f_Nfactor, t_Nfactor, h_Nfactor, friends, tbbt, himym)
    test(testDataH, f_Nfactor, t_Nfactor, h_Nfactor, friends, tbbt, himym)


def test(testData,f_Nfactor, t_Nfactor, h_Nfactor, friends, tbbt, himym):

    result = []
    for sentence in testData:
        print(sentence)
        report = classifier(sentence,f_Nfactor, t_Nfactor, h_Nfactor, friends, tbbt, himym)

        if report.count(0.0) != 3:                  # if it's not [0,0,0]
            print(report)
            print(report.index(max(report)))        # predict which series it belongs to
            result.append(report.index(max(report)))

    print(len(testData))
    print(len(result))

    print('friends: ' + str(result.count(0)))
    print('tbbt: ' + str(result.count(1)))
    print('himym: ' + str(result.count(2)))
    return result


# calculate the likelihood of a given sentence in each serie.
def classifier(sentence, f_Nfactor, t_Nfactor, h_Nfactor, friends, tbbt, himym):

    f_fix = 0.9248
    t_fix = 1.0853
    f_prob = probability(sentence, friends, f_Nfactor)
    t_prob = probability(sentence, tbbt, t_Nfactor)
    h_prob = probability(sentence, himym, h_Nfactor)

    return [f_prob*f_fix, t_prob*t_fix, h_prob]



def probability(sentence, show, nFactor):

    # tokenize the words and filter out the words that are not in vocabulary (show)
    words = nltk.word_tokenize(sentence)
    wordBag = []

    for word in words:
        if word not in string.punctuation and word in show:  # and word not in stopwords.words("english"):  # ignore the words not in vocab?
            # wordBag_puncFree.append(porter.stem(word))   # stem?
            wordBag.append(word)
    print(wordBag)
    t = len(wordBag)


    if t == 0:
        return 0

    contextWords = []
    for w in wordBag:
        contextWords.append(w)

    probability = 0

    for centerWord in wordBag:
        contextWords.remove(centerWord)  #only remove once the occurrance
        #print('\n')
        #print('centerWord: ' + centerWord)
        #print(contextWords)

        cWordVec = show.get_vector(centerWord)
        normalizer = np.abs(cWordVec.dot(nFactor).item())
        #absNormalizer = np.abs(normalizer).item() # convert numpy float32 to float #do abs in stead of exp

        # probability algorithm
        prob = 0
        for word in contextWords:
            sim = cWordVec.dot(show.get_vector(word))
            #print('\n')
            #print('contextWord: '+ word)

            absSim = np.abs(sim.item())
            p = absSim/normalizer        # log
            #print('absSim: ' + str(absSim) + ' absNorm:' + str(normalizer))
            #print('p: '+ str(p))

            prob = prob + p
            #print('prob of ' + centerWord + ': '+ str(prob))                             # for a center word

        #print('end prob: ' + str(prob))

        probability = probability + prob                            # for a sentence
        #print('Sentence probability: ' + str(probability))
        contextWords.append(centerWord)

    #print('result: ' + str(probability))
    return probability/t

# generate word2Vec model on the data sets, save to temp file.
# pay attention to how to arrange the temp file.
# pay attention: keyedvectors should be generated from the correct temp file
def generateW2V(trainDataF, trainDataT, trainDataH):

    friendW2V = generate(trainDataF, 'friends.bin')
    tbbtW2V = generate(trainDataT, 'tbbt.bin')
    himymW2V = generate(trainDataH, 'himym.bin')


def generate(sentences, tmp_File):

    phr = Phrases()
    # only first 80% for the sentence
    bags = []
    for sentence in sentences:
        wordBag = nltk.word_tokenize(sentence)  #cut sentence in words
        wordBag_puncFree = []
        for word in wordBag:
            if word not in string.punctuation : #and word not in stopwords.words("english"):
                # wordBag_puncFree.append(porter.stem(word))   # stem?
                wordBag_puncFree.append(word)
                phr.add_vocab([wordBag_puncFree])
        bags.append(wordBag_puncFree)

    #dataProcess.printLines(list(phr[bags]))
    #print(len(f0101))
    #print(len(bags))

    w2v = Word2Vec(phr[bags], min_count=1, size=200)
    #Word2Vec(common_texts, size=100, window=5, min_count=1, workers=4)   window?
    word_vectors = w2v.wv

#tempfile.TemporaryFile()

    fname =  get_tmpfile(tmp_File)
    word_vectors.save(fname)
    wv = KeyedVectors.load(fname, mmap='r')

#C:\Users\Dina\PycharmProjects\NLP_RP\w2v\friends.bin

def cutList(list, ratio):

    tot = len(list)
    cut = math.floor(tot*ratio)
    trainData = list[:cut]
    testData = list[cut:]
    return (trainData, testData)

# vectors of all words in vocabulary, add together as normalization- factor
def getNormFactor(show):

    #print('has: ' + str(len(show.vocab)) + ' words')

    count = 0
    sum = np.zeros(200, dtype="float32")

    for word in show.vocab:
        count= count +1
        sum = sum + show.get_vector(word)

   #return sum/count
    return sum






# just trying out
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