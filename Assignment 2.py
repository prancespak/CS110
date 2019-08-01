import math 
import mmh3 
from bitarray import bitarray 
from statistics import mean
import matplotlib.pyplot as plt
from random import shuffle

class BloomFilter(object): 
    #the way this implementation works is that the bloom filter uses the
    #functions in the wiki article to create the optimal bitarray size and
    #use the otpimal number of hash functions
    def __init__(self, items_count,falsep_prob): 
        self.falsep_prob = falsep_prob # false positive probability
        self.size = self.get_size(items_count,falsep_prob) # how large the bit array should be (using formula)
        self.hash_count = self.get_hash_count(self.size,items_count) # how many hash functions to use (using formula)
        self.bit_array = bitarray(self.size) #set bit array to given size
        self.bit_array.setall(0) #bit array is empty, so everything is set to 0

    def add(self, element): 
        for i in range(self.hash_count): #should run hash function as many times as is hash_count
            index = mmh3.hash(element,i) % self.size #run hash func with i as seed
            self.bit_array[index] = 1 #bit at the index should be 1
        return self
        
    def lookup(self, element): 
        isitthere = True 
        for i in range(self.hash_count): #do same as in add function
            index = mmh3.hash(element, i) % self.size
            if self.bit_array[index] == 0: #but instead of changing the bit
                isitthere = False #you check if the bit is 1 or 0. if it is 0, the element is not here

        return isitthere
    
    def get_size(self,n,p): 
        #get the optimal bit array size
        m = -(n * math.log(p))/(math.log(2)**2) #formula from the wiki page
        return int(m) 

    def get_hash_count(self, m, n): 
        #the optimal number of hash functions
        k = (m/n) * math.log(2) #formula found on the wiki page
        return int(k) 

def general(p, inlist, notinlist):
    #define n
    n = len(inlist) #this is how many things we're going to add
#the desired probability of false positives
    
    bloom = BloomFilter(n, p) #create bloom filter
    
    for element in inlist:
        bloom.add(element) #add all the elements in the list to the bloom filter
    
    print ("Bit array size: {}".format(bloom.size))
    print("Initial false positive probability:{}".format(bloom.falsep_prob)) 
    print("Number of hash functions to use:{}".format(bloom.hash_count))
    
    checkingwords = inlist + notinlist
    shuffle(checkingwords)
    
    false_positives = 0 #make a counter to see how many false positives
    
    for word in checkingwords:
        if bloom.lookup(word) is True: #if the word is in the bit array
            if word in notinlist: #but the word is not actually in the list
                false_positives += 1
                print ("'{}' is a false positive".format(word)) #its a false positive
            else: #otherwise it's actually in there
                print("'{}' is probably there".format(word))
        else: #or if its not there, it's definitely not in the array
            print("'{}' is definitely not there".format(word))
    
    print ("Number of false positives: {}".format(false_positives))

inlist = makelist(20)
notinlist = makelist(20)

general(0.1, inlist, notinlist)


# TEST AND PLOTS
import random
import string

#Implementation that takes out all the unnecessary things from the first implementation for the trials
def main(n, p):
    
    bloom = BloomFilter(n, p)
    return bloom.size

def makelist(n): #function to make a list of random 6 letter strings
    list = []
    for i in range(n):
        list.append(''.join(random.choice(string.ascii_lowercase) for i in range(6)))
    return list

inlist = makelist(20) #a list of strings that will be in the bloom filter
notinlist = makelist(20) #a list of strings that will NOT be in the bloom filter
                        #will count false positives with this

###
### TEST 1: memory size as a function of the false positive rate
###

testfpperc = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5] #false positive rates

task1 = []
for test in testfpperc: #for all the false positive rates above,
    task1.append(main(20, test)) #run the main implementation with them

%matplotlib inline
#plot the results
plt.plot(testfpperc,task1)
plt.ylabel('Bitarray Size')
plt.xlabel('False Positive Rate')
plt.show()

###
### TEST 2: memory size as a function of the number of items stored
###

#list of the number of elements to put into the bitarray
the_ns = [10, 50, 100, 150, 200, 250]
task2 = []
for ns in the_ns: #for the different values of n
    task2.append(main(ns, 0.05)) #run them as input in the main function

#plot the results
plt.plot(the_ns,task2)
plt.ylabel('Bitarray Size')
plt.xlabel('Items Added')
plt.show()


###
### TEST 3: access time as a function of the false positive rate
###

import time

#an adapted version of the first implementation
#it performs lookup, but doesn't do all the extra printing
def adapted(p, inlist, notinlist):
    n = len(inlist)
    
    bloom = BloomFilter(n, p)
    
    for element in inlist:
        bloom.add(element)
    
    checkingwords = inlist + notinlist
    shuffle(checkingwords)
    
    false_positives = 0
    
    for word in checkingwords:
        if bloom.lookup(word) is True: 
            if word in notinlist: 
                false_positives += 1
    return float(false_positives)/len(checkingwords)

inlist = makelist(20)
notinlist = makelist(20)

#list of false positive rates
fprates = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
accesstime = []
for i in fprates: 
    start_time = time.time()
    adapted(i, inlist, notinlist) #run the general function with the false pos rates as input
    accesstime.append(time.time() - start_time) #measure the time taken and add to the list

#plot the results
plt.plot(fprates,accesstime)
plt.ylabel('Access Time')
plt.xlabel('False Positive Rates')
plt.show()


###
### TEST 4: access time as a function of the number of items stored
###

inlist = makelist(20)
notinlist = makelist(20)

#the different number of elements to add to the bitarray
the_ns = [10, 50, 100, 150, 200, 250]
accesstimes = []

for i in the_ns:
    start_time = time.time()
    adapted(0.1, makelist(i), makelist(i)) #run the general function with the inputs
    #standard probability of false pos of 0.1
    accesstimes.append(time.time() - start_time) #record the times

#plot the results
plt.plot(the_ns,accesstimes)
plt.ylabel('Access Time')
plt.xlabel('Number of Inputs')
plt.show()


# produce a plot to show that your implementation's false positive
# rate matches the theoretically expected rate.

inlist = makelist(25)
notinlist = makelist(25)

#theoretical false positivee rates
theoreticalrates = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5,]

#function to get average
def getaverage(p):
    result = []
    for i in range(50): #getting the average of actual false positives for 10 trials
        result.append(adapted(p, inlist, notinlist))
    return float(mean(result))

#get the average of average, so that the results are more accurate
def averageofaverage(p):
    results = []
    for i in range(50):
        results.append(getaverage(p))
    return float(mean(results))

actualfp = [] #actual false positive rates

#run the general function with the theoretical rates as inputs
for i in range(0, 6):
    actualfp.append(averageofaverage(theoreticalrates[i]))

#plot the results
plt.plot(theoreticalrates, actualfp)
plt.ylabel('Actual FP Rates')
plt.xlabel('Theoretical FP Rates')
plt.show()
