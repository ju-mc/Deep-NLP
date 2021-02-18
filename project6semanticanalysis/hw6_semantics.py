import nltk
import sys
import re
from nltk.tokenize import word_tokenize
import io
from nltk.parse import FeatureEarleyChartParser


def open_sentences(sentencesFile):
# open sentences file
    sentences = open(sentencesFile, 'r')
    #sentences = sentences.readlines()
    return sentences

def open_outputfile(outfile):
#open output file
    outfile = open(outfile, 'w')
    return outfile

def load(grammarFile, outfile):
#this function loads the grammar and uses the FeatureEarleyChartParser from nltk

    grammar = nltk.data.load(grammarFile, format='fcfg')
    parser = nltk.parse.FeatureEarleyChartParser(grammar)

    return parser

def parse(sen, parser):
#tokenize each word in each sentence, then parse using those tokens
    tokens = nltk.word_tokenize(sen)
    for j in parser.parse(tokens):
        return j.label()['SEM'].simplify()
    return ''

def main():
    sentencesFile = sys.argv[2]
    sentences = open_sentences(sentencesFile)
    sentence_lst = []
    for i in sentences:
        sentence_lst.append(i)
    
    grammarFile = sys.argv[1]

    outfile = sys.argv[3]
    outfile = open_outputfile(outfile)
    
    parser = load(grammarFile, outfile)
    #final = parse(tokens, parser)
    for sen in sentence_lst:
        outfile.write(sen)
        final = parse(sen, parser)
        outfile.write("{}\n".format(final))
if __name__=='__main__':
    main()
