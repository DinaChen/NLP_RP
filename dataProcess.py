import re
import csv
import os

angleBrac = '<(.|\n)*?>'        # remove <>
roundBrac = '\(([^)]+)\)'       # remove()
squareBrac = '\[(.|\n)*?\]'     #remove[]
# remove number?
noice = '(&.*;)|(Commercial Break)|(Commercial break)|' \
        '(Closing Credits)|(CLOSING CREDITS)|(Opening Credits)|' \
        '(OPENING TITLES)|(.push;)|(THE END)|[0-9]' #[0-9]

# &#151; appears in 0118, &#146; appears in 16, .push; in tbbt

def main():

    path = 'C:/Users/Dina/PycharmProjects/NLP_RP/How I Met Your Mother/season1/0106.html'




def bigbang():
    path = 'C:/Users/Dina/PycharmProjects/NLP_RP/The Big Bang Theory/season1'
    filePaths = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.html' in file:
                filePaths.append(os.path.join(r, file))

    tbbt = seasonTranscript(filePaths, 'tbbt')
    printLines(tbbt)
    print('#lines: ' + str(len(tbbt)))
    print('#episodes: ' + str(len(filePaths)))
    print('avg.lines per episode: ' + str(len(tbbt) / len(filePaths)))

def friends():
    path = 'C:/Users/Dina/PycharmProjects/NLP_RP/transcripts/season2'
    filePaths = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.html' in file:
                filePaths.append(os.path.join(r, file))

    friends = seasonTranscript(filePaths, 'friends')
    printLines(friends)
    print('#lines: ' + str(len(friends)))
    print('#episodes: ' + str(len(filePaths)))
    print('avg.lines per episode: ' + str(len(friends) / len(filePaths)))

# Given transcript of 1 season in html format, out put list of lines with all irrelevant info removed, all episodes concatenate together.
# List(html_path) -> List(string)
def seasonTranscript(listOfpath, serie):
    toreturn = []
    for epi in listOfpath:
        if(serie == 'friends'):
            toreturn = toreturn + episodeTranscript(epi)
        elif(serie == 'tbbt'):
            toreturn = toreturn + epiTranscript((epi))

    return toreturn


# for the big bang theory, how I met your mother
def epiTranscript(html_path):
    epi = open(html_path, encoding="utf8").read()
    scene_removed = re.sub('(<p>Scene|<p><strong>).*', "", epi)  #second one for himym
    #scene_removed1 = re.sub('<p>.*:', '<p>', scene_removed)
    lines = re.findall('<p>.*', scene_removed)
    toreturn = []
    for line in lines:
        cleanedline = re.sub('.*:', "", cleaned(line))
        if cleanedline:                                         #no empty line added
            toreturn.append(cleanedline.lower())                # to lowercase
    return toreturn


# episodeTranscript is for Friends only
# Given transcript of 1 episode in html format, out put list of lines with all irrelevant info removed.
# .html_path -> List(string)
def episodeTranscript(html_path):
    epi = open(html_path, 'r').read()
    cleaned_transcript = cleaned(epi).lower()
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
            k = re.sub('(End)|(END)|(THE END)', '', j)
            toreturn.append(k)
        else:
            toreturn.append(j)

    return toreturn

#remove all the punctuation
def removePunctuation(text):
    return re.sub("[^\w\s]", "", text)



# print list of string in readable way
def printLines(epi):
    for line in epi:
       print(line)


main()
