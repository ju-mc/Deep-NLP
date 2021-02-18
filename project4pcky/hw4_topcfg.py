import sys
import math
import io
import nltk
import pprint
import collections

def open_sentences(sentencesFile):
#open treebank
    sentences = open(sentencesFile,'r')
    sentences = sentences.readlines()
    return sentences


def get_probabilities(p_lst):
    
    #create a dictionary to store probabilities for each production
    dict = {}
    count = collections.Counter()

    lefths = collections.Counter()
    pr_lst = []

    
    for i in p_lst:
        #track occurrences of i in the list of productions
        count[i] += 1
        lefths[i.lhs()] += 1


    for j in count:
       #calculate probabilities
       prob = float(count[j]/lefths[j.lhs()])
       
       #use nltk probabilisticProduction -- production with an associated probability
       final_pr = nltk.grammar.ProbabilisticProduction(j.lhs(),j.rhs(),prob=prob)
       pr_lst.append(final_pr)
       dict[j] = float(count[j]/lefths[j.lhs()])

    #return pcfg grammar with specified starting point
    return nltk.grammar.PCFG(nltk.grammar.Nonterminal('TOP'),pr_lst)
    

def main():
    sentence_lst = []
    sentencesFile = sys.argv[1]
    sentences = open_sentences(sentencesFile)
    for i in sentences:
        i = i.replace('\n','')
        sentence_lst.append(i)

    p_lst = []
    
    #add trees corresponding to each sentence to list (p_lst)
    for j in sentence_lst:
        tree = nltk.tree.Tree.fromstring(j)
        for prod in tree.productions():
            p_lst.append(prod)

    rules_w_probs = get_probabilities(p_lst)

    outfile = sys.argv[2]
    outp = open(outfile, 'w')
    
    outp.write('%start TOP\n')
    
    #write to output file
    for prod in rules_w_probs.productions():
        outp.write(str(prod)+'\n')
    
if __name__=='__main__':
    main()

