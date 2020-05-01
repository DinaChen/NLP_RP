import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
import os
import os.path as op
import math

#test train ratio: 8:2
ratio = 0.8


fpaths = ['embeddedFriends/friends0101']
tpaths = ['embeddedTBBT/0101.csv']
hpaths = ['embeddedHIMYM/0101.csv']

train_and_test(fpaths, tpaths, hpaths)




def train_and_test(fPaths, tPaths, hPaths):

    fSet = paths_toDF(fPaths)
    tSet = paths_toDF(tPaths)
    hSet = paths_toDF(hPaths)
    (fTrain,fTest) = divideTrainTest(fSet)
    (tTrain,tTest) = divideTrainTest(tSet)
    (hTrain,hTest) = divideTrainTest(hSet)

    # make senctences_x
    sentencesTrain = pd.concat([fTrain, tTrain, hTrain])
    sentencesTest = pd.concat([fTest, tTest, hTest])

    # make labels
    fTrain_count = fTrain.shape[0]
    tTrain_count = tTrain.shape[0]
    hTrain_count= hTrain.shape[0]
    labelsTrain = makeLabels(fTrain_count, tTrain_count, hTrain_count)

    fTest_count = fTest.shape[0]
    tTest_count = tTest.shape[0]
    hTest_count= hTest.shape[0]
    labelsTest = makeLabels(fTest_count, tTest_count, hTest_count)

    # Print data information
    print('Train Set: f :'+ str(fTrain_count) + ' t: '+ str(tTrain_count) + ' h: ' + str(hTrain_count))
    print('Tot: ' + str(fTrain_count+tTrain_count+hTrain_count) + ' labels: ' + str(labelsTrain.shape[0]) + ' train: ' + str(sentencesTrain.shape[0]))
    print('Test Set: f: ' + str(fTest_count) + ' t: ' + str(tTest_count) + ' h: ' + str(hTest_count))
    print('Tot: '+ str(fTest_count + tTest_count + hTest_count) + ' labels: ' + str(labelsTest.shape[0]) + ' test: ' + str(sentencesTest.shape[0]))

    #啊啊啊魔法啊展现你的力量吧

    logReg = LogisticRegression(max_iter = 4000)
    logReg.fit(sentencesTrain, labelsTrain.values.ravel())
    labelsPred = logReg.predict(sentencesTest)
    successRate = metrics.accuracy_score(labelsTest, labelsPred)
    #print(labelsPred)
    print('Success rate: '+ str(successRate*100))


# divide data to train and test set
def divideTrainTest(df):

    c = df.shape[0]
    trainCount = math.floor(c*ratio)

    trainSet = df.head(trainCount)
    testSet = df.tail(c - trainCount)

    #print(trainSet.shape)
    #print(testSet.shape)

    return trainSet, testSet


# input: list of path containing sentence embeddings. csv file
# output: one dataframe
def paths_toDF(paths):
    dfs = []
    for path in paths:
        df = pd.read_csv(path, sep='|', header=None)
        dfs.append(df)

    return pd.concat(dfs)

# make train/test labels for the corresponding data set
# input: amount of instances of friends/tbbt/himym.
def makeLabels(friends, tbbt, himym):

    f=[]
    for i in range(friends):
        f.append("f")

    t=[]
    for i in range(tbbt):
        t.append("t")

    h=[]
    for i in range(himym):
        h.append("h")

    df = pd.concat([pd.DataFrame(f), pd.DataFrame(t), pd.DataFrame(h)])
    return df

def getAllpaths(scriptFile):
    #path = 'C:/Users/Dina/PycharmProjects/NLP_RP/transcripts/season2'
    filePaths = []
    for r, d, f in os.walk(scriptFile):
        for file in f:
            if '.csv' in file:
                filePaths.append(os.path.join(r, file))
    return filePaths







# How you concatenate two data frame
    #labels = ['F', 'F', 'F']
    #labels1 = ['H', 'H', 'H']
    #df = pd.DataFrame(labels)
    #df1 = pd.DataFrame(labels1)
    #con = pd.concat([df, df1])
    #print(con)
# How to split data frame
#Note you can also use df.head(10) and df.tail(len(df) - 10) to get the front and back according to your needs.
    #print(con.head(2)) #first two row
    #print(con.tail(len(con)-2)) # the rest




# Create linear regression object
#regr = linear_model.LinearRegression()

# Train the model using the training sets
#regr.fit(sentencesTrain, labelsTrain)

# Make predictions using the testing set
#labelsPred = regr.predict(sentencesTest)


