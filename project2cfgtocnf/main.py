#Juliana McCausland
#ling 571
#hw 2

import nltk
import sys
import copy
import os.path
import six
import re

label_inventory = []
prod_dict = {}

def longer_productions():
#this function locates long productions
#and adds substitute non-terminals (i.e. X), creates new rules using the substituted values,
#and adds valid items to grammar (production dictionary)
        count = 0
        dictcopy = copy.deepcopy(prod_dict)
        for i in dictcopy:
                dicti = dictcopy[i]
                for j in range(len(dicti)):
                        if len(dicti[j]) > 2:
                                for x in range(0,len(dicti[j])-2):
                                        if x == 0:
                                                lst = []
                                                lst.append(prod_dict[i][j][0])
                                                sub = 'X' + str(count)
                                                lst.append(sub)
                                                count += 1
                                                prod_dict[i][j] = lst
                                        else:
                                                lst = []
                                                lst.append(dicti[j][x])
                                                sub = 'X' + str(count)
                                                lst.append(sub)
                                                count += 1
                                                prod_dict.setdefault(dcopy,[]).append(lst)
                                        label_inventory.append(sub)
                                        dcopy = copy.deepcopy(sub)
                                prod_dict[dcopy]=[]
                                prod_dict[dcopy].append(dicti[j][-2:])
def other_productions():
#this function locates short productions and removes as necessary, finalizing cnf rules 
        track = 1
        while track:
                track = 0
                dictcopy = copy.deepcopy(prod_dict)
                for i in dictcopy:
                        copya = dictcopy[i]
                        for j in range(len(copya)):
                                if len(copya[j]) == 1 and copya[j][0] in label_inventory and copya[j][0] != i:
                                        dc = copy.deepcopy(copya[j][0])
                                        prod_dict[i].remove(copya[j])
                                        dca = prod_dict[dc]
                                        for x in range(len(dca)):
                                                prod_dict[i].append(dca[x])
                for i in prod_dict:
                        copya = prod_dict[i]
                        for j in range(len(copya)):
                                if len(copya[j])==1 and copya[j][0]in label_inventory and copya[j][0]!=prod_dict[copya[j][0]]:
                                        track=1
                                        break
                        if track:
                                break

def main():
        atiscfg = sys.argv[1]
        grammar = nltk.data.load(atiscfg)
        #fill label inventory and production dictionary with items from the loaded grammar
        for i in range(len(grammar.productions())):
                k = grammar.productions()[i].lhs()
                k = str(k)
                v = list(grammar.productions()[i].rhs())
                for i in range(len(v)):
                        #using isinstance to identify strings in grammar
                        if isinstance(v[i],str):
                                v[i] = "'" + v[i] + "'"
                        else:
                                v[i] = str(v[i])
                if k not in label_inventory:
                        label_inventory.append(k)
                        prod_dict[k]=[v]
                elif v not in prod_dict[k]:
                        prod_dict[k].append(v)
                        
        longer_productions()
        other_productions()
        
        #write to output file
        outp = open(sys.argv[2], 'w')
        #for k, v in prod_dict.items():
                #outp.write("{} -> {}".format(k,v))
        for i in prod_dict:
                content = prod_dict[i]
                for j in range(len(content)):
                        txt =''
                        txt += i +' -> '+ str(content[j]) +'\n'
                        #txt = re.sub(r'\,', ' ', txt)
                        leftbrackets = r'\[*'
                        rightbrackets = r'\]*'
                        leftapost = ' \'*'
                        rightapost = '\'*'
                        txt = re.sub(leftbrackets, '', txt)
                        txt = re.sub(rightbrackets, '', txt)
                        txt = re.sub(leftapost, ' ', txt)
                        txt = re.sub(rightapost, '', txt)
                        txt = re.sub(r'\,', ' ', txt)
                        outp.write(txt)


if __name__=='__main__':

        main()


