import re
import csv
#remove irrelevant information, only dialogue self will be left over
##### To remove:
# Title lines, writtenby, transcripbed by.... End

# Charactor:

# punctuation? not yet

# input: 1 html file :
# later: a list of html file for whole serie
# output: list of sentence?
# use Pickle?
# first all sentence

# problem: cant open the big bang theory file
# question: do i have to download the script one by one?

angleBrac = '<(.|\n)*?>'  # remove <>
roundBrac = '\(([^)]+)\)'  # remove()
squareBrac = '\[(.|\n)*?\]'  # '\[.*?\]'  #remove[]  doesn't completely work yet
noice = '(&nbsp;)|(&quot;)'

def main():

    ep1 = 'transcripts/friends0101.html'
    ep2 = 'transcripts/friends0102.html'
    #bb = open('transcripts/tbbt0101.html', encoding="utf8").read()

    s1 = episodeTranscript(ep1)
    printLines(s1)


# then group everything together as 1 string
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
    toreturn = []
    for line in splitted:
        j = re.sub('\n', "", line)
        toreturn.append(j)
    #print(toreturn)
    return toreturn


# print list of string in readable way
def printLines(epi):
    for line in epi:
       print(line)


main()