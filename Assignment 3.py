###Write python code to give the length of the 
###longest common subsequence for two strings.

import itertools
from tabulate import tabulate

def lcs(x , y): 
    # find the length of the strings 
    m = len(x) 
    n = len(y) 
  
    #create table b that will store the values
    b = [[None]*(n+1) for i in xrange(m+1)] 
    
    #for each element in x
    for i in range(m+1): 
        #for each element in y
        for j in range(n+1):
            #fill first row and column with 0
            if i == 0 or j == 0 : 
                b[i][j] = 0
            #then +1 to the NW
            elif x[i-1] == y[j-1]: 
                b[i][j] = b[i-1][j-1]+1
            #otherwise get the max between either left or top
            else: 
                b[i][j] = max(b[i-1][j] , b[i][j-1]) 
  
   #returns the longest common subsequence of the two strings
    return b[m][n]

###Generate the table of the lengths of the 
###longest common subsequences for every pair of strings.


genelist = [(0, 'CAGCGGGTGCGTAATTTGGAGAAGTTATTCTGCAACGAAATCAATCC'
                'TGTTTCGTTAGCTTACGGACTACGACGAGAGGGTACTTCCCTGATATAGTCAC'), 
(1, 'CAAGTCGGGCGTATTGGAGAATATTTAAATCGGAAGATCATGTTACTATGCGTTAGC'
    'TCACGGACTGAAGAGGATTCTCTCTTAATGCAA'), 
(2, 'CATGGGTGCGTCGATTTTGGCAGTAAAGTGGAATCGTCAGATATCAATCCTGTTTCGT'
    'AGAAAGGAGCTACCTAGAGAGGATTACTCTCACATAGTA'), 
(3, 'CAAGTCCGCGATAAATTGGAATATTTGTCAATCGGAATAGTCAACTTAGCTGGCGTT'
    'GCTTTACGACTGACAGAGAGAAACCTGTCCATCACACA'), 
(4, 'CAAGTCCGGCGTAATTGGAGAATATTTTGCAATCGGAAGATCAATCTTGTTAGCGTT'
    'AGCTTACGACTGACGAGAGGGATACTCTCTCTAATACAA'), 
(5, 'CACGGGCTCCGCAATTTTGGGTCAAGTTGCATATCAGTCATCGACAATCAAACACTGT'
    'TTTGCGGTAGATAAGATACGACTGAGAGAGGACGTTCGCTCGAATATAGTTAC'), 
(6, 'CACGGGTCCGTCAATTTTGGAGTAAGTTGATATCGTCACGAAATCAATCCTGTTTCG'
    'GTAGTATAGGACTACGACGAGAGAGGACGTTCCTCTGATATAGTTAC')]

x = [] #pairs
y = [] #LCS

#make a table initialized with None
table = [[None for i in range(7)]for i in range(7)]

#combinations gets only the unique pairs (i.e. 0,1 and 1,0 
# are only counted once)
for pair in itertools.combinations(genelist, 2):
    #add the pair to list x
    x.append([j[0] for j in pair])
    #add the LCS for the pair to y
    y.append(lcs(*(x[1] for x in pair))) 

###Filling the table

#for all 21 pairs
for i in range(0,21):
    #define horizontal index
    h = x[i][0]
    #define vertical index
    v = x[i][1]
    #place the LCS in appropriate spot on table
    table[h][v] = y[i]

print tabulate(table, headers=('0','1','2','3','4','5','6'), 
               tablefmt='fancy_grid', showindex="always")
               
###Tree algorithm


def get_tree(pairings, values):
    sums = [] #total LCS sums
    tree = [] #ordering of tree
    
    #for each gene
    for i in range(0,7):
        #will be collecting LCSs to sum
        to_sum = []
        #for each of the gene's pairs
        for pair in pairings:
            #get vertical and horizontal index
            h = pair[0]
            v = pair[1]
            #if one of the pairs includes the gene
            if i == h or i == v:
                #then add the value to to_sum list
                to_sum.append(values[h][v])
        #get sum and add to total        
        sums.append(sum(to_sum))

    #for the # of genes
    for j in range(0,7):
        #places indexes in order so that two largest elements are middle nodes
        #third largest is root node
        #and rest are distributed as leaves
        if len(tree) == 0 or len(tree) == 1 or len(tree) >= 3:
            k = sums.index(max(sums))
            tree.append(k)
            sums[k] = 0
        elif len(tree) == 2:
            k = sums.index(max(sums))
            tree.insert(0, k)
            sums[k] = 0
    return tree
    

print get_tree(x, table)
