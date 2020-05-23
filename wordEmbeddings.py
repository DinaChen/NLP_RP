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
# lancaster = LancasterStemmer()
# porter = PorterStemmer()

def main():

    # Split train and test set
    friends_data = dataProcess.friends()
    tbbt_data = dataProcess.bigbang()
    himym_data = dataProcess.himym()

    friends_Sets = np.array_split(friends_data, 5)
    tbbt_Sets = np.array_split(tbbt_data, 5)
    himym_Sets = np.array_split(himym_data, 5)

    # Fold 1
    friends_test1 = friends_Sets[0]
    tbbt_test1 = tbbt_Sets[0]
    himym_test1 = himym_Sets[0]

    friends_train1 = np.concatenate([friends_Sets[1], friends_Sets[2], friends_Sets[3], friends_Sets[4]])
    tbbt_train1 = np.concatenate([tbbt_Sets[1], tbbt_Sets[2], tbbt_Sets[3], tbbt_Sets[4]])
    himym_train1 = np.concatenate([himym_Sets[1], himym_Sets[2], himym_Sets[3], himym_Sets[4]])

    #generateW2V(friends_train1, tbbt_train1, himym_train1, 'friends1.bin', 'tbbt1.bin', 'himym1.bin')
    #runTest('friends1.bin','tbbt1.bin','himym1.bin', friends_test1, tbbt_test1, himym_test1)

    # Fold 2
    friends_test2 = friends_Sets[1]
    tbbt_test2 = tbbt_Sets[1]
    himym_test2 = himym_Sets[1]
    friends_train2 = np.concatenate([friends_Sets[0],friends_Sets[2], friends_Sets[3], friends_Sets[4]])
    tbbt_train2 = np.concatenate([tbbt_Sets[0], tbbt_Sets[2], tbbt_Sets[3], tbbt_Sets[4]])
    himym_train2 = np.concatenate([himym_Sets[0], himym_Sets[2], himym_Sets[3], himym_Sets[4]])

    #generateW2V(friends_train2, tbbt_train2, himym_train2, 'friends2.bin', 'tbbt2.bin', 'himym2.bin')
    #runTest('friends2.bin', 'tbbt2.bin', 'himym2.bin', friends_test2, tbbt_test2, himym_test2)

    # Fold 3
    friends_test3 = friends_Sets[2]
    tbbt_test3 = tbbt_Sets[2]
    himym_test3 = himym_Sets[2]
    friends_train3 = np.concatenate([friends_Sets[0],friends_Sets[1], friends_Sets[3], friends_Sets[4]])
    tbbt_train3 = np.concatenate([tbbt_Sets[0], tbbt_Sets[1], tbbt_Sets[3], tbbt_Sets[4]])
    himym_train3 = np.concatenate([himym_Sets[0], himym_Sets[1], himym_Sets[3], himym_Sets[4]])
    #generateW2V(friends_train3, tbbt_train3, himym_train3, 'friends3.bin', 'tbbt3.bin', 'himym3.bin')
    #runTest('friends3.bin', 'tbbt3.bin', 'himym3.bin', friends_test3, tbbt_test3, himym_test3)

    # Fold 4
    friends_test4 = friends_Sets[3]
    tbbt_test4 = tbbt_Sets[3]
    himym_test4 = himym_Sets[3]
    friends_train4 = np.concatenate([friends_Sets[0],friends_Sets[1], friends_Sets[2], friends_Sets[4]])
    tbbt_train4 = np.concatenate([tbbt_Sets[0], tbbt_Sets[1], tbbt_Sets[2], tbbt_Sets[4]])
    himym_train4 = np.concatenate([himym_Sets[0], himym_Sets[1], himym_Sets[2], himym_Sets[4]])
    #generateW2V(friends_train4, tbbt_train4, himym_train4, 'friends4.bin', 'tbbt4.bin', 'himym4.bin')
    runTest('friends4.bin', 'tbbt4.bin', 'himym4.bin', friends_test4, tbbt_test4, himym_test4)

    # Fold 5
    friends_test5 = friends_Sets[4]
    tbbt_test5 = tbbt_Sets[4]
    himym_test5 = himym_Sets[4]
    friends_train5 = np.concatenate([friends_Sets[0],friends_Sets[1], friends_Sets[2], friends_Sets[3]])
    tbbt_train5 = np.concatenate([tbbt_Sets[0], tbbt_Sets[1], tbbt_Sets[2], tbbt_Sets[3]])
    himym_train5 = np.concatenate([himym_Sets[0], himym_Sets[1], himym_Sets[2], himym_Sets[3]])
    #generateW2V(friends_train5, tbbt_train5, himym_train5, 'friends5.bin', 'tbbt5.bin', 'himym5.bin')
    runTest('friends5.bin', 'tbbt5.bin', 'himym5.bin', friends_test5, tbbt_test5, himym_test5)


def runTest(fpath, tpath, hpath, ftest, ttest, htest):

    friends = KeyedVectors.load(get_tmpfile(fpath), mmap='r')
    tbbt = KeyedVectors.load(get_tmpfile(tpath), mmap='r')
    himym = KeyedVectors.load(get_tmpfile(hpath), mmap='r')

    balancers = getBalancer(len(friends.vocab), len(tbbt.vocab), len(himym.vocab))

    t_Nfactor = getNormFactor(tbbt)
    f_Nfactor = getNormFactor(friends)
    h_Nfactor = getNormFactor(himym)

    test(ftest, f_Nfactor, t_Nfactor, h_Nfactor, friends, tbbt, himym, balancers)
    #test(ttest, f_Nfactor, t_Nfactor, h_Nfactor, friends, tbbt, himym, balancers)
    #test(htest, f_Nfactor, t_Nfactor, h_Nfactor, friends, tbbt, himym, balancers)


def result2():

    # Split train and test set
    friends_data = dataProcess.friends()
    tbbt_data = dataProcess.bigbang()
    himym_data = dataProcess.himym()

    # Train word2Vec on the last 80% of data
    (testDataF, trainDataF) = cutList(friends_data, 0.2)
    (testDataT, trainDataT) = cutList(tbbt_data, 0.2)
    (testDataH, trainDataH) = cutList(himym_data, 0.2)

    #generateW2V(trainDataF, trainDataT, trainDataH)        Only need to execute once
    friends1 = KeyedVectors.load(get_tmpfile('friends_1.bin'), mmap='r')
    tbbt1 = KeyedVectors.load(get_tmpfile('tbbt_1.bin'), mmap='r')
    himym1 = KeyedVectors.load(get_tmpfile('himym_1.bin'), mmap='r')

    #print('Friends has: ' + str(len(friends1.vocab)) + ' words')
    #print('The Big Bang Theory has: ' + str(len(tbbt1.vocab)) + ' words')
    #print('How I met Your Mother has: ' + str(len(himym1.vocab)) + ' words')

    balancers = getBalancer(len(friends1.vocab), len(tbbt1.vocab), len(himym1.vocab))

    t_Nfactor1 = getNormFactor(tbbt1)
    f_Nfactor1 = getNormFactor(friends1)
    h_Nfactor1 = getNormFactor(himym1)

    #test(testDataF, f_Nfactor1, t_Nfactor1, h_Nfactor1, friends1, tbbt1, himym1, balancers)
    #test(testDataT, f_Nfactor1, t_Nfactor1, h_Nfactor1, friends1, tbbt1, himym1, balancers)
    #test(testDataH, f_Nfactor1, t_Nfactor1, h_Nfactor1, friends1, tbbt1, himym1, balancers)

    # Result: (see Skip gram experiment log _ Result 2)
    #         18505 / 38429 = 0.481537380624


def result1():

    # Split train and test set
    friends_data = dataProcess.friends()
    tbbt_data = dataProcess.bigbang()
    himym_data = dataProcess.himym()

    # Train word2Vec on the first 80% of data
    (trainDataF, testDataF) = cutList(friends_data, 0.8)
    (trainDataT, testDataT) = cutList(tbbt_data, 0.8)
    (trainDataH, testDataH) = cutList(himym_data, 0.8)

    # generateW2V(trainDataF, trainDataT, trainDataH)     Only need to execute once

    # Get KeyedVectors of word2Vec embeddings
    # Only punctuation removal.
    friends = KeyedVectors.load(get_tmpfile('friends.bin'), mmap='r')
    tbbt = KeyedVectors.load(get_tmpfile('tbbt.bin'), mmap='r')
    himym = KeyedVectors.load(get_tmpfile('himym.bin'), mmap='r')

    # Get normalizing factor (add up all the words in the vocabulary together)
    t_Nfactor = getNormFactor(tbbt)
    f_Nfactor = getNormFactor(friends)
    h_Nfactor = getNormFactor(himym)

    balancers = getBalancer(len(friends.vocab), len(tbbt.vocab), len(himym.vocab))

    #test(testDataF, f_Nfactor, t_Nfactor, h_Nfactor, friends, tbbt, himym, balancers)
    #test(testDataT, f_Nfactor, t_Nfactor, h_Nfactor, friends, tbbt, himym, balancers)
    test(testDataH, f_Nfactor, t_Nfactor, h_Nfactor, friends, tbbt, himym, balancers)

    # Result: (see Skip gram experiment log _ Result 1)
    #         19541 / 38885 = 0.50253311



def test(testData,f_Nfactor, t_Nfactor, h_Nfactor, friends, tbbt, himym, balancers):

    result = []
    for sentence in testData:
        print(sentence)
        report = classifier(sentence,f_Nfactor, t_Nfactor, h_Nfactor, friends, tbbt, himym, balancers)

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
def classifier(sentence, f_Nfactor, t_Nfactor, h_Nfactor, friends, tbbt, himym, balancers):

    f_balancer = balancers[0]
    t_balancer = balancers[1]
    h_balancer = balancers[2]

    f_prob = probability(sentence, friends, f_Nfactor)
    t_prob = probability(sentence, tbbt, t_Nfactor)
    h_prob = probability(sentence, himym, h_Nfactor)

    return [f_prob*f_balancer, t_prob*t_balancer, h_prob*h_balancer]



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
    if t == 1:
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

        probability = probability + prob #/(t-1)                      # for a sentence
        #print('Sentence probability: ' + str(probability))
        contextWords.append(centerWord)

    #print('result: ' + str(probability))
    return probability/t

# generate word2Vec model on the data sets, save to temp file.
# pay attention to how to arrange the temp file.
# pay attention: keyedvectors should be generated from the correct temp file
def generateW2V(trainDataF, trainDataT, trainDataH, fpath, tpath, hpath):

    friendW2V = generate(trainDataF, fpath)
    tbbtW2V = generate(trainDataT, tpath) #'tbbt_1.bin
    himymW2V = generate(trainDataH, hpath)


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

    print('has: ' + str(len(show.vocab)) + ' words')

    count = 0
    sum = np.zeros(200, dtype="float32")

    for word in show.vocab:
        print(word)
        count= count +1
        sum = sum + show.get_vector(word)

   #return sum/count
    return sum


def getBalancer(f, t, h):
    tot = f + t + h
    f_rate = f / tot
    t_rate = t / tot
    h_rate = h / tot

    fbalancer = 1 + (f_rate - 1/3)
    tbalancer = 1 + (t_rate - 1/3)
    hbalancer = 1 + (h_rate - 1/3)

    print(fbalancer)
    print(tbalancer)
    print(hbalancer)

    return [fbalancer, tbalancer, hbalancer]


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


#result2()
main()
#tokenize()
#spacy()