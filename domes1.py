##stable 1.0
##pretty much deployable :)
from random import seed
from random import randint
import random
import numpy as np
import array
import os

comparisons = 0

myFilename = 'tucBinaryFinal.bin'

M = 500
N = 2**18
K = 10**3

def fileIsEmpty(): #checks if the file is empty by looking at the .bin's size
    if (os.path.getsize(myFilename) == 0):
        return True
    else:
        return False

def page(n): #more compact way to seek(), returns the number of pages multiplied by 256
    return (n)*256

class Node: #node class storing the coordinates
    def __init__(self, data_x, data_y):
        self.data_x = data_x
        self.data_y = data_y
        self.next = None


class LinkedList: #linked list holding the head and the tail
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data_x, data_y): #appends the coordinates 
        node = Node(data_x, data_y) #create a node with the coords

        if not self.head: #if the list is empty, create a node and consider it the head
            self.head = node
        else:
            self.tail.next = node #add the new node after the tail
        self.tail = node #added node becomes the tail

# search function that goes through each node, comparing the x and y values of the node with
#the ones given by the user

    def search(self, user_x, user_y):
        global comparisons
        searches = 0
        found = 0
        temp = self.head #temp variable to help traverse the LL
        while temp is not None:
            searches += 1 #1 comparison
            if temp.data_x == user_x and temp.data_y == user_y:
                searches += 2 #2 comparisons, one for x and one for y
                found = 1
                break
            searches += 2 #2 comparisons, one for x and one for y, either this or the one under the if statement fires
            temp = temp.next
        comparisons += searches #number of comparisons is added to the total
        return found


class HashTable():
    def __init__(self):
        self.hashtable = np.array([None]*N) #HT is an N-sized array
        for x in range(M):
            self.hashtable[x] = LinkedList() #create a LL at every index of the HT

    def getHash(self, x, y): #gets the has value of the (x,y) pair
        H = (x*N + y) % M
        return H

    def insertKey(self, x, y): #inserts key by calling the linked list's append method to the index given by the hash
        index = self.getHash(x, y)
        self.hashtable[index].append(x, y)

    def searchNode(self, x, y):
        index = self.getHash(x, y) #looks for a key by calling the linked list's search method to the index given by the hash
        return self.hashtable[index].search(x, y)

def readBytes(file, position): #reads 256 bytes (a disk page) at the given position 
	file.seek(position)
	byte_array = bytearray(file.read(256))
	return byte_array

def toIntArray(bytes): #turns a bytearray into an integer list with calling Python's built-in methods to 4-byte-chunks of the bytearray
	result = [0 for i in range(64)] # total of 64 numbers
	for i in range(0, 64):
		result[i] = int.from_bytes(bytes[i*4:i*4+4], 'little')
	return result

def toBytes(intArray): #turns an integer array into bytes
	result = array.array('B', range(0,256))
	for i in range(0, 64):
		bytesOfInt = intArray[i].to_bytes(4, byteorder='little') #turns one of intArray's ints into 4 bytes, and assigns each byte to its respective place in the result array
		result[i*4] = bytesOfInt[0]
		result[i*4+1] = bytesOfInt[0+1]
		result[i*4+2] = bytesOfInt[0+2]
		result[i*4+3] = bytesOfInt[0+3]
	return result

def writeBytes(file, bytes, position): #writes bytearray at given position
	file.seek(position)
	bytes = file.write(bytes)

def hasSpace(lastDiskPage): #checks if the diskpage has any space left by looking for a 2**19 (number out of bounds for the RNG), if spotted, it returns True, else, returns false
    has_space = False
    with open(myFilename, 'rb') as file:
        bytes = readBytes(file, page(lastDiskPage))
        intArray = toIntArray(bytes)
    for i in range(64):
        if (intArray[i] == 2**19):
            has_space = True
            break
    return has_space

def lastIndex(lastDiskPage): #reads the last disk page, turns its contents into integers, enters them into an array, and then returns the first index with the value of 2**19 (same logic as above)
    with open(myFilename, 'rb') as file:
        bytes = readBytes(file, page(lastDiskPage))
        intArray = toIntArray(bytes)
        for i in range(64):
            if (intArray[i] == 2**19):
                return i

class Lista: #class for the B1 question

    tucBuffer = [2**19 for i in range(64)]
    
    def __init__(self): #initializes tail and head with -1, meaning that it's empty
        self.head = -1
        self.tail = -1
        self.searches = 0 #searches to print out total comparisons

    def bufferSize(self):
        for i in range(64):
            if (self.tucBuffer[i] == 2**19):
                return i
        return 64
    
    def add(self, x, y):
        if (self.bufferSize() == 64): #when the buffer fills up
            if (fileIsEmpty()):
                self.head = 0
                self.tail = 0
            self.writeToDisk() #data is written to the disk
            self.tucBuffer = [2**19 for i in range(64)] #the buffer is reset
            self.tail += 1
        self.tucBuffer[self.bufferSize()] = x
        self.tucBuffer[self.bufferSize()] = y

    def forceWrite(self):
        self.writeToDisk() #data is written
        self.tucBuffer = [2**19 for i in range(64)] #buffer reset

    def writeToDisk(self):
        if (fileIsEmpty()):
            self.head = 0
            self.tail = 0
        bytes = toBytes(self.tucBuffer)
        with open(myFilename, 'ab') as file:
            writeBytes(file, bytes, page(self.tail))

def main():
    file = open(myFilename, 'w') #creates the file without risking errors
    file.close()
    with open(myFilename, 'r+') as file: #clears the file by setting its size to 0
        file.truncate(0)
    listoula = Lista()

    print('~'*5,"Linked List",'~'*5)
    l = LinkedList()
    elementsInTheLinkedList = [] #creating a list of all the elements in the LL
    for i in range (0,K): #populating the LL and the disk with K random elements
        c = random.randrange(0,N)
        d = random.randrange(0,N)
        l.append(c, d)
        listoula.add(c, d)
        elementsInTheLinkedList.append(c)
        elementsInTheLinkedList.append(d)
    listoula.forceWrite()
    hundredRandomElementsInLL = []
    for i in range(0,100): #searching for 100 random pairs from the LL
        randomIndex = random.randrange(0, int(K/2))
        hundredRandomElementsInLL.append(elementsInTheLinkedList[int(randomIndex*2)])
        hundredRandomElementsInLL.append(elementsInTheLinkedList[int(randomIndex*2)+1])
    for i in range(0,100):
        l.search(hundredRandomElementsInLL[i*2], hundredRandomElementsInLL[(i*2)+1])
        l.search(random.randrange(N,N+100), random.randrange(N,N+100))
    print("LL comparisons:", comparisons)

    print('~'*5,"Hashtable",'~'*5)
    HT = HashTable()
    elementsInTheHashTable = []
    for i in range (0,K): #populating the HT with K random elements
        c = random.randrange(0,N) #picks 2 random integers
        d = random.randrange(0,N)
        HT.insertKey(c, d) #adds them to the hashtable
        elementsInTheHashTable.append(c) #logs them in the respective list
        elementsInTheHashTable.append(d)
    hundredRandomElementsInHT = []
    for i in range(0,100): #searching for 100 random pairs from the HT
        randomIndex = random.randrange(0, int(K/2)) #picks an index, doubles it (meaning it's always an x), and adds it and its respective y to the list
        hundredRandomElementsInHT.append(elementsInTheHashTable[int(randomIndex*2)]) #exact same logic is used in the linked list test searches
        hundredRandomElementsInHT.append(elementsInTheHashTable[int(randomIndex*2)+1])
    for i in range(0,100):
        HT.searchNode(hundredRandomElementsInHT[i*2], hundredRandomElementsInHT[(i*2)+1])
        HT.searchNode(random.randrange(N,N+100), random.randrange(N,N+100))
    print("Total comparisons:", comparisons)
        

if __name__ == "__main__":
    main()
