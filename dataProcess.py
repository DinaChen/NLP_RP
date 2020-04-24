import re
import csv
import os

angleBrac = '<(.|\n)*?>'        # remove <>
roundBrac = '\(([^)]+)\)'       # remove()
squareBrac = '\[(.|\n)*?\]'     #remove[]
noice = '(&.*;)|(Commercial Break)|(Commercial break)|(Closing Credits)|(CLOSING CREDITS)|(Opening Credits)|(OPENING TITLES)'
#noice = '(&nbsp;)|(&quot;)|(Commercial Break)|(Commercial break)|(Closing Credits)|(Opening Credits)|(&#146;)|(&#151;)'
# &#151; appears in 0118, &#146; appears in 16

def main():
    path = 'C:/Users/Dina/PycharmProjects/NLP_RP/transcripts/'
    filePaths = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.html' in file:
                filePaths.append(os.path.join(r, file))


    friends = seasonTranscript(filePaths)
    printLines(friends)
    print('#lines: ' + str(len(friends)))
    print('#episodes: ' + str(len(filePaths)))
    print('avg.lines per episode: ' + str(len(friends)/len(filePaths)))

#bb = open('transcripts/tbbt0101.html', encoding="utf8").read()



# Given transcript of 1 season in html format, out put list of lines with all irrelevant info removed, all episodes concatenate together.
# List(html_path) -> List(string)
def seasonTranscript(listOfpath):
    toreturn = []
    for epi in listOfpath:
        toreturn = toreturn + episodeTranscript(epi)
    return toreturn



# Given transcript of 1 episode in html format, out put list of lines with all irrelevant info removed.
# .html_path -> List(string)
def episodeTranscript(html_path):
    epi = open(html_path, 'r').read()
    cleaned_transcript = cleaned(epi)
    splitted_transcript = split(cleaned_transcript)
    return splitted_transcript


# remove brackets and weird sign (&nbsp;, &quot;)
# remove things at once
# string -> string
def cleaned(epi):
    t1 = re.sub(angleBrac, "", epi)
    t2 = re.sub(roundBrac, "", t1)
    t3 = re.sub(squareBrac, "", t2)
    t4 = re.sub(noice, "", t3)
    return t4


# use "Character:" as delimeter to cut transcript of one episode into seperated lines
# for every line substitute \n with ''
# string -> List[string]
def split(epi):
    deli = '.*:'
    splitted = re.split(deli, epi)

    #Remove first 3 lines (written by:, transcript by:)
    splitted.remove(splitted[0])
    splitted.remove(splitted[0])
    splitted.remove(splitted[0])

    toreturn = []
    for line in splitted:

        j = re.sub('\n', " ", line)

        if splitted.index(line) == len(splitted)-1:
            k = re.sub('(End)|(END)', '', j)
            toreturn.append(k)
        else:
            toreturn.append(j)

    return toreturn


# print list of string in readable way
def printLines(epi):
    for line in epi:
       print(line)


main()