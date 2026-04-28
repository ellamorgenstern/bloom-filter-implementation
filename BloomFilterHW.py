from BitHash import BitHash
from BitVector import BitVector

class BloomFilter(object):
    # Return the estimated number of bits needed (N in the slides) in a Bloom 
    # Filter that will store numKeys (n in the slides) keys, using numHashes 
    # (d in the slides) hash functions, and that will have a
    # false positive rate of maxFalsePositive (P in the slides).
    # See the slides for the math needed to do this.  
    # You use Equation B to get the desired phi from P and d
    # You then use Equation D to get the needed N from d, phi, and n
    # N is the value to return from bitsNeeded
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        
        n = numKeys
        d = numHashes
        P = maxFalsePositive
        
        #Equation B to get desirve phi -> Phi = (1 - P^(1/d))
        phi = 1-P**(1/d)
        
        #Equation D to get the needed N -> N = d / (1-Phi^(1/n))
        N = d / ( 1 - phi**(1/n))
        
        #return N for bit bitsNeeded
        return int(N)
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        # will need to use __bitsNeeded to figure out how big
        # of a BitVector will be needed
        # In addition to the BitVector, might you need any other attributes?
        
        self.__numKeys = numKeys #n
        self.__numHashes = numHashes #d
        self.__maxFalsePositive = maxFalsePositive #P
        
        self.__vectorSize = \
            self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)
        self.__bitVector = BitVector(size=self.__vectorSize)
        self.__bits = 0        
        
    
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    # See the "Bloom Filter details" slide for how insert works.
    def insert(self, key):
        
        #For i = 1 .. d set the bit at position H[i](key) % N
        
        for i in range(1, self.__numHashes + 1): #start at 1
            
            # hash the key numHash number of times
            h = BitHash(key,i)
            pos = h % self.__vectorSize
            
            #if there was nothing in pos than set to 1
            if self.__bitVector[pos] == 0:
                self.__bitVector[pos] = 1
                
                #add number of bits
                self.__bits += 1
            
    
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.
    # See the "Bloom Filter details" slide for how find works.
    def find(self, key):
        
        #For i = 1 .. d check the bit at position Hi(key) % N
        for i in range(1, self.__numHashes + 1): #start at 1
            
            h = BitHash(key,i)
            pos = h % self.__vectorSize
            
            # If any bit is 0 than key is definetely not in Bloom filter
            if self.__bitVector[pos] == 0:
                return False
        
        #if none are 0 than key is probably in Bloom filter    
        return True
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits actually set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # measuring the proportion of false positives that are actually encountered.
    # In other words, you use equation A to give you P from d and phi. 
    # What is phi in this case? it is the ACTUAL measured current proportion 
    # of bits in the bit vector that are still zero. 
    def falsePositiveRate(self):
        
        d = self.__numHashes
        
        #find the current phi 
        phi = (self.__vectorSize - self.__bits) / self.__vectorSize
        
        #use equation A to find projected false Positive rate
        projectedP = (1 - phi)**d
        
        return projectedP
       
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    # WHEN TESTING, MAKE SURE THAT YOUR IMPLEMENTATION DOES NOT CAUSE
    # THIS PARTICULAR METHOD TO RUN SLOWLY.
    def numBitsSet(self):
        
        return self.__bits


       

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    # create the Bloom Filter
    bloomF = BloomFilter(numKeys, numHashes, maxFalse)
    
    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    f = open("wordlist.txt")
    line = f.readline()
    count = 0
    
    #loop through each line in file until finished or count reaches numKeys
    while line and count< numKeys:
        
        word = line.strip()
        
        #insert into bloom filter
        bloomF.insert(word)
        
        count+=1
        line = f.readline()
        

    #Close file    
    f.close()

    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. Use the falsePositiveRate method.
    print("The projected false positive rate is "+ str(bloomF.falsePositiveRate()))

    # Now re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. This should report that 0 words are 23
    # missing from the Bloom Filter. Don't close the input file of words since
    # in the next step we want to read the next numKeys words from the file. 
    f = open("wordlist.txt")
    line = f.readline()
    count = 0
    missing = 0
    #loop through each line in file until finished or count reaches numKeys
    while line and count< numKeys:
        
        word = line.strip()
        
        #count if word is missing 
        #if find returns False, than not found
        if not bloomF.find(word): 
            
            #add to missing count
            missing+=1
        
        count+=1
        line = f.readline()
        
         
    print(str(missing) + " words are missing from the Bloom Filter")
    
    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    
    #count for the words falsely found
    falseFind = 0 
    
    #count rest of words in file
    countRest = 0
    
    #loop through rest of bloomFilter
    while line and countRest < numKeys:
        
        word = line.strip()
        
        #if word falsely found 
        if bloomF.find(word):
            falseFind += 1
            
        countRest += 1
        line = f.readline()
        
    falsePosRate = falseFind / countRest
    
    # Print out the percentage rate of false positives.
    # THIS NUMBER MUST BE CLOSE TO THE ESTIMATED FALSE POSITIVE RATE ABOVE
    
    print("The percentage rate of false positives is " + str(falsePosRate))
    
    #Close file        
    f.close()

    
if __name__ == '__main__':
    __main()       

