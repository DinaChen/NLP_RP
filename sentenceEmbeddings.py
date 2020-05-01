import tensorflow_hub as hub
import tensorflow as tf
import tensorflow.compat.v1 as tf
import os
import os.path as op
import csv
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import dataProcess

def main():

 tf.disable_eager_execution()

 scriptPaths = ['How I Met Your Mother/season1/0101.html', 'How I Met Your Mother/season1/0102.html','How I Met Your Mother/season1/0103.html',
                'How I Met Your Mother/season1/0104.html','How I Met Your Mother/season1/0105.html']    # create a list of unparsed files                   for example:  ['The Big Bang Theory/season1/0105.html']
 csvPaths = ['embeddedHIMYM/0101.csv','embeddedHIMYM/0102.csv','embeddedHIMYM/0103.csv','embeddedHIMYM/0104.csv'
             ,'embeddedHIMYM/0105.csv']       # create a list of the csv file it should write to, for example:  ['embeddedTBBT/0105.csv']

 embeddingsForeach(scriptPaths, csvPaths)



# scriptPaths: a list of paths of unparsed script
# csvPaths: a list of path to write the results to,
def embeddingsForeach(scriptPaths, csvPaths):
    tf.disable_eager_execution()
    for (i,j) in zip(scriptPaths, csvPaths):
       parsed = dataProcess.epiTranscript(i)            # friends : episodeTranscript
       elmoVec_toCSV(parsed,j)


# given list of parsed transcript. write the result of elmo_vectors() to file -- given as the second parameter.
def elmoVec_toCSV(parsedTranscript, embeddedPath):
    embedded = elmo_vectors(parsedTranscript)
    embeddedDF = pd.DataFrame(embedded)
    embeddedDF.to_csv(embeddedPath, sep='|', header=False, index=False)

# input: a list of string: parsed transcript.
# output: a list of vectors.
# every string(sentence) in the input list is transformed into vector.
def elmo_vectors(x):
  elmo = hub.Module("https://tfhub.dev/google/elmo/2", trainable=True)
  embeddings = elmo(x, signature="default", as_dict=True)["elmo"]

  with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    sess.run(tf.tables_initializer())

    return sess.run(tf.reduce_mean(embeddings,1))

# given a file path, retrieves a list of all the paths it contains.
def getAllpaths(scriptFile):
    #path = 'C:/Users/Dina/PycharmProjects/NLP_RP/transcripts/season2'
    filePaths = []
    for r, d, f in os.walk(scriptFile):
        for file in f:
            if '.html' in file:
                filePaths.append(os.path.join(r, file))
    return filePaths

main()
