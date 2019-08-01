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
