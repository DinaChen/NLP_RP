import re
import csv
#remove irrelevant information, only dialogue self will be left over
# use Pickle?
# first all sentence


angleBrac = '<(.|\n)*?>'        # remove <>
roundBrac = '\(([^)]+)\)'       # remove()
squareBrac = '\[(.|\n)*?\]'     #remove[]
noice = '(&.*;)|(Commercial Break)|(Commercial break)|(Closing Credits)|(Opening Credits)'
#noice = '(&nbsp;)|(&quot;)|(Commercial Break)|(Commercial break)|(Closing Credits)|(Opening Credits)|(&#146;)|(&#151;)'
# &#151; appears in 0118, &#146; appears in 16

def main():

    ep1 = 'transcripts/0101.html'
    ep2 = 'transcripts/0102.html'
    ep3 = 'transcripts/0103.html'
    ep4 = 'transcripts/0104.html'
    ep5 = 'transcripts/0105.html'
    ep6 = 'transcripts/0106.html'
    ep7 = 'transcripts/0107.html'
    ep8 = 'transcripts/0108.html'
    ep9 = 'transcripts/0109.html'
    ep10 = 'transcripts/0110.html'
    ep11 = 'transcripts/0111.html'
    ep12 = 'transcripts/0112.html'
    ep13 = 'transcripts/0113.html'
    ep14 = 'transcripts/0114.html'
    ep15 = 'transcripts/0115.html'
    ep16 = 'transcripts/0116.html'
    ep17 = 'transcripts/0117.html'
    ep18 = 'transcripts/0118.html'
    ep19 = 'transcripts/0119.html'
    ep20 = 'transcripts/0120.html'
    ep21 = 'transcripts/0121.html'
    ep22 = 'transcripts/0122.html'
    ep23 = 'transcripts/0123.html'
    ep24 = 'transcripts/0124.html'

    #bb = open('transcripts/tbbt0101.html', encoding="utf8").read()

    friendS1_paths = [ep1, ep2, ep3, ep4, ep5, ep6, ep7, ep8, ep9, ep10, ep11, ep12, ep13, ep14, ep15, ep16, ep17, ep18, ep19, ep20, ep21, ep22, ep23, ep24]
    friendS1 = seasonTranscript(friendS1_paths)
    printLines(friendS1)
    print(len(friendS1))


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

        j = re.sub('\n', "", line)

        if splitted.index(line) == len(splitted)-1:
            k = re.sub('End', '', j)
            toreturn.append(k)
        else:
            toreturn.append(j)

    return toreturn


# print list of string in readable way
def printLines(epi):
    for line in epi:
       print(line)


main()