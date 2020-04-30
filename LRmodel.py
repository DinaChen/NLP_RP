import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
import os
import os.path as op

def main():

    friends0101 = pd.read_csv('embeddedFriends/friends0101', sep='|', header=None)
    tbbt0101 = pd.read_csv('embeddedTBBT/0101.csv', sep='|', header=None)
    himym0101 = pd.read_csv('embeddedHIMYM/0101.csv', sep='|', header=None )

    friends0101_train = friends0101.head(243)
    friend0101_test = friends0101.tail(len(friends0101)-243)
    tbbt0101_train = tbbt0101.head(260)
    tbbt0101_test = tbbt0101.tail(len(tbbt0101) - 260)
    himym0101_train = himym0101.head(220)
    himym0101_test = himym0101.tail(len(himym0101) -220)

    sentencesTrain = pd.concat([friends0101_train, tbbt0101_train, himym0101_train])
    sentencesTest = pd.concat([friend0101_test, tbbt0101_test, himym0101_test])
    labelsTrain = makeLabels(243, 220, 260)
    labelsTest = makeLabels(61, 56, 67)

    logReg = LogisticRegression(max_iter = 4000)
    logReg.fit(sentencesTrain, labelsTrain.values.ravel())
    labelsPred = logReg.predict(sentencesTest)
    successRate = metrics.accuracy_score(labelsTest, labelsPred)
    print(labelsPred)
    print(successRate*100)





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


main()