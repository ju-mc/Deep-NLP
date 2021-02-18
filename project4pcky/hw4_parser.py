import nltk
import sys
from nltk.grammar import CFG, Production, Nonterminal, PCFG

Empty = None

class Node:

    def __init__(self, root, token, left, right, prob):
        self.root = root
        self.left = left
        self.right = right
        self.token = token
        self.prob = prob
        
def open_sentences(sentencesFile):
    sentences = open(sentencesFile, 'r')
    return sentences
    
def open_outputfile(outfile):
    outfile = open(outfile, 'w')
    return outfile

def parse_cyk(start, grammar, sent):
#this function performs the primary cky algorithm using a table (T) and a pointer, which will be used for parsing.
#hw4 update: added probabilities (note addition to Node class)
    final_p = ''
    length = len(sent)
    
    T = [[[] for i in range(length+1)] for j in range(length+1)]
    
    pointerT = [[[] for i in range(length+1)] for j in range(length+1)]
    
    for num in range(1,length+1):
        for rule in grammar:
            lhs = rule._lhs
            
            if sent[num-1] in rule._rhs:
                T[num-1][num].append(lhs)
                pointerT[num-1][num].append(Node(lhs, sent[num-1], Empty, Empty, float(rule.prob())))
                
                
        for j in reversed(range(0,num-1)):
            for x in range(j+1,num):
                for rule in grammar:
                    lhs = rule._lhs
                    
                    
                    if len(rule._rhs) == 2:
                        if rule._rhs[0] in T[j][x] and rule._rhs[1] in T[x][num]:
                            T[j][num].append(lhs)
                            for pval1 in pointerT[j][x]:
                                for pval2 in pointerT[x][num]:
                                    if pval1.root == rule._rhs[0] and pval2.root == rule._rhs[1]:
                                        pointerT[j][num].append(Node(rule._lhs, Empty, pval1, pval2, float(rule.prob())*pval1.prob * pval2.prob))
                                        
    ct = 0
    #make a tree for the span of the sentence from the back pointer from the 0th element to the last element
    trees = pointerT[0][length]
    reach = 0.0
    n = Empty
    
    #get the parse for each tree, accounting for empty trees as well (creating empty string)
    for i in trees:
        if i.prob > reach:
            ct +=1
            reach = i.prob
            n = i
    if n != Empty:
        t = get_tree(n)
        t = ' '.join(str(t).split())
    else:
        t = ' '
 
    return str(t)
    
    
def get_tree(n):

    if n.token == Empty:
        tr = nltk.tree.Tree(str(n.root), [get_tree(n.left), get_tree(n.right)])
        return tr
        
    else:
        t = nltk.tree.Tree(str(n.root), [str(n.token)])
        return t


def main():
    
    sentencesFile = sys.argv[2]
    sentences = open_sentences(sentencesFile)
    
    strng = ''
    grammar_file = sys.argv[1]
    
    outfile = sys.argv[3]
    outfile = open_outputfile(outfile)
    
    grammar = open(grammar_file, 'r')
    for i in grammar:
        strng += i
    #input pcfg as strings
    grammar = PCFG.fromstring(strng)
    
    for i in sentences:
        tokens = nltk.word_tokenize(i)
        
        final_p = parse_cyk(grammar.start(), grammar.productions(), tokens)
        outfile.write(final_p+"\n")

if __name__ == "__main__":
    main()

