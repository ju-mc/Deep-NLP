#Juliana McCausland
#Ling 571
#HW1

import nltk
import sys
import re
from nltk.tokenize import word_tokenize
import io


def open_sentences(sentencesFile):
# open sentences file and read them into a list called 'sentences'
    sentences = open(sentencesFile, 'r')
    sentences = sentences.readlines()
    return sentences

def open_outputfile(outfile):
    outfile = open(outfile, 'w')
    return outfile

def load_and_parse(grammarFile, sentences, outfile):

#this function loads the grammar and uses the EarleyChartParser from nltk,
#tokenizes the sentences (also using nltk), and then parses each token.
#It returns the average number of parses (total)

    lst = []
    #load grammar and create earley chart parser
    grammar = nltk.data.load(grammarFile)
    parser = nltk.parse.EarleyChartParser(grammar)

    sentence_lst = []
    for i in sentences:
        count = 0
        outfile.write('\n{}'.format(i)) 
        sentence_lst.append(i)
        tokens = nltk.word_tokenize(i) #tokenize each sentence for parsing


        #print('%s'%i)
        for j in parser.parse(tokens):
            count +=1
            outfile.write(str(j)+'\n')
        outfile.write('Number of parses: {}\n'.format(count))

        lst.append(count)

    sum_of_all_parses = sum(lst)
    length_of_lst = len(lst)

    return sum_of_all_parses/length_of_lst  #return avg number of parses

def main():
    sentencesFile = sys.argv[2]
    sentences = open_sentences(sentencesFile)

    grammarFile = sys.argv[1]

    outfile = sys.argv[3]
    outfile = open_outputfile(outfile)

    avg = load_and_parse(grammarFile, sentences, outfile)
    outfile.write("\nAverage number of parses: {}\n".format(round(avg, 3)))

if __name__=='__main__':
    main()
