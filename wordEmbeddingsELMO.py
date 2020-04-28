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
    transcriptPath = 'transcripts/season1/0102.html'
    embeddedPath = 'embeddedFriends/friends0102'
    parsedTranscript = dataProcess.episodeTranscript(transcriptPath)
    dataProcess.printLines(parsedTranscript)


    elmoVec_toCSV(parsedTranscript, embeddedPath)



def elmoVec_toCSV(parsedTranscript, embeddedPath):

    embedded = elmo_vectors(parsedTranscript)
    embeddedDF = pd.DataFrame(embedded)
    embeddedDF.to_csv(embeddedPath, sep='|', header=False, index=False)
    print(elmo_vectors(x))


def elmo_vectors(x):
  elmo = hub.Module("https://tfhub.dev/google/elmo/2", trainable=True)
  embeddings = elmo(x, signature="default", as_dict=True)["elmo"]

  with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    sess.run(tf.tables_initializer())

    return sess.run(tf.reduce_mean(embeddings,1))

main()
