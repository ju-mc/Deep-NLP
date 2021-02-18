import nltk
import os
import sys

Empty = None

class Node:

    def __init__(self, root, token, begin, end, left, right):
        self.root = root
        self.token = token
        self.begin = begin
        self.end = end
        self.left = left
        self.right = right
                 
def open_sentences(sentencesFile):
    sentences = open(sentencesFile, 'r')
    return sentences

def open_outputfile(outfile):
    outfile = open(outfile, 'w')
    return outfile


def parse_cyk(start, grammar, sent):
#this function performs the primary cky algorithm using a table (T) and a pointer, which will be used
#for parsing.
    Empty = None
    length = len(sent)
    #print("INPUT SENTENCE: ", sent)
    
    T = [[[] for i in range(length+1)] for j in range(length+1)]
    
    pointerT = [[[] for i in range(length+1)] for j in range(length+1)]
    
    for num in range(1,length+1):
        for rule in grammar:
            lhs = rule._lhs
            
            if sent[num-1] in rule._rhs:
                T[num-1][num].append(lhs)
                pointerT[num-1][num].append(Node(lhs, sent[num-1], num-1, num-1, Empty, Empty))
                
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
                                        pointerT[j][num].append(Node(rule._lhs, Empty, pval1.begin, pval1.end, pval1, pval2))
    #make a tree for the span of the sentence from the back pointer from the 0th element to the last element
    trees = pointerT[0][length]
    count = 0
    n = Empty
    strng = ''
    for i in trees:
        n = i
    if n != Empty:
        count += 1
        #pass string of values to parse to get_tree fucntion
        strng += str(get_tree(n))

    return strng, count
        
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
        
    grammarFile = sys.argv[1]
    grammar = nltk.data.load(grammarFile)
    productions = grammar.productions()
    start = grammar.start()

    outfile = sys.argv[3]
    outfile = open_outputfile(outfile)
    counts = []
    
    for i in sentences:
        tokens = nltk.word_tokenize(i)
        outfile.write("\n" + i)

        p_final, count = parse_cyk(start, productions, tokens)
           
        outfile.write(p_final + "\n" + "Number of parses: " + str(count) + "\n")


    #sen = nltk.data.load(sys.argv[2])
    #H = nltk.parse.util.extract_test_sentences(sen)

if __name__=='__main__':
    main()

