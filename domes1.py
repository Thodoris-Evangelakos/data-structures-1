##stable 0.1
##NEAR DEPLOYABLE
##molis prosthetw ena zeugos, koitaw to teleutaio disk page tou arxeiou, an
from random import seed
from random import randint
import random
import numpy as np
import array
import os

##100 searches gia stoixeia pou einai mesa kai 100 gia stoixeia pou den einai

comparisons = 0

myFilename = 'tucBinaryFinal.bin'

M = 500
N = 2**18
Buffer = []
tempBuffer = []

def fileIsEmpty():
    if (os.path.getsize(myFilename) == 0):
        return True
    else:
        return False

def page(n):
    return (n)*256

class Node:
    def __init__(self, data_x, data_y):
        self.data_x = data_x
        self.data_y = data_y
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data_x, data_y):
        node = Node(data_x, data_y)

        if not self.head:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node

    def printList(self):
        temp = self.head
        if not temp:
            print(None)
        while temp:
            if temp.next:
                print("(%d,%d)" %
                      (self.head.data_x, self.head.data_y), "--->", end="  ")
            else:
                print("(%d,%d)" % (self.head.data_x, self.head.data_y))
            temp = temp.next

# search function that goes through each node, comparing the x and y values

    def search(self, user_x, user_y):
        global comparisons
        searches = 0
        found = 0
        temp = self.head
        while temp is not None:
            searches += 1
            if temp.data_x == user_x and temp.data_y == user_y:
                searches += 2
                found = 1
                break
            searches += 2
            temp = temp.next
        comparisons += searches
        print("Searches:",searches)
        return found


class HashTable():
    def __init__(self):
        self.hashtable = np.array([None]*N)
        for x in range(M):
            self.hashtable[x] = LinkedList()

    def getHash(self, x, y):
        H = (x*N + y) % M
        #print("H(%d,%d) = %d" %(x, y ,H))
        return H

    def insertKey(self, x, y):
        index = self.getHash(x, y)
        self.hashtable[index].append(x, y)

    def searchNode(self, x, y):
        index = self.getHash(x, y)
        print("Index of (%d,%d): %d" % (x, y, self.getHash(x, y)))
        print("Searching at given index...")
        return self.hashtable[index].search(x, y)

    def printHashTable(self):
        print("Hash table is :- \n")
        print("Index \t\tValues\n")
        for x in range(M):
            print(x, end="\t\t")
            self.hashtable[x].printList()

def readBytes(file, position):
	file.seek(position) 
	byte_array = bytearray(file.read(256)) #ERWTHSH: to bytearray metatrepei kati se array apo bytes, alla afou kanoume read apo .bin prepei hdh na einai se bytes(?)
	return byte_array

def toIntArray(bytes):
	result = [0 for i in range(64)] # total of 64 numbers
	for i in range(0, 64):
		result[i] = int.from_bytes(bytes[i*4:i*4+4], 'little')
	return result

def toBytes(intArray):
	result = array.array('B', range(0,256))
	for i in range(0, 64):
		bytesOfInt = intArray[i].to_bytes(4, byteorder='little')
		result[i*4] = bytesOfInt[0]
		result[i*4+1] = bytesOfInt[0+1]
		result[i*4+2] = bytesOfInt[0+2]
		result[i*4+3] = bytesOfInt[0+3]
	return result

def writeBytes(file, bytes, position):
	file.seek(position)
	bytes = file.write(bytes)

###EXP
#def addToBuffer(x, y):
#    if len(tempBuffer) < 64:
#        tempBuffer.append(x)
#        tempBuffer.append(y)
#    else:
#        bytes = toBytes(tempBuffer)
#
#def addToLL(ll, x, y):
#    ll = LinkedList()
#    ll.append(x, y)
#
#def addToHT(HT, x, y):
#    HT = HashTable()
#    HT.insertKey(x, y)

def hasSpace(lastDiskPage):
    with open(myFilename, 'rb') as file:
        bytes = readBytes(file, page(lastDiskPage))
        intArray = toIntArray(bytes)
    for i in range(0,63):
        if (intArray[i] == 2**19):
            return True
        else:
            return False

def lastIndex(lastDiskPage):
    with open(myFilename, 'rb') as file:
        bytes = readBytes(file, lastDiskPage*256)
        intArray = toIntArray(bytes)
        for i in range(0,63):
            if (intArray[i] == 2**19):
                return i
            else:
                return i

class Lista:
    def __init__(self):
        self.head = -1
        self.tail = -1
    
    def add(self, x, y):
        if fileIsEmpty(): #an head OR tail -1 einai adeio to list
            self.head = 0 #prepei na phgainei sto telos tou arxeiou, megethos arxeiou / 256
            self.tail = 0 #to idio me to panw
            #skipped to 2)
            newBuffer = [2**19 for i in range(64)]
            newBuffer[0] = x
            newBuffer[1] = y
            bytes = toBytes(newBuffer)
            with open(myFilename, 'wb') as file:
                writeBytes(file, bytes, self.tail)
            newBuffer.clear()
        else:
            if (hasSpace(self.tail)):
                newBuffer = []
                #1)
                ##fortwnw sto buffer o,ti yparxei sto diskage kai sto telos tou vazw ta x y mou
                with open(myFilename, 'rb') as file:
                    bytes = readBytes(file, page(self.tail))
                    newBuffer = toIntArray(bytes)
                newBuffer[lastIndex(self.tail)] = x
                newBuffer[lastIndex(self.tail)+1] = y
                with open(myFilename, 'wb') as file:
                    bytes = toBytes(newBuffer)
                    writeBytes(file, bytes, page(self.tail))
                #write back to disk
            else:
                newBuffer = [2**19 for i in range(64)]
                newBuffer.append(0)
                newBuffer.append(1)
                bytes = toBytes(newBuffer)
                with open(myFilename, 'wb') as file:
                    writeBytes(file, bytes, page(self.tail+1))
                self.tail += 1
                newBuffer.clear()

def main():
    with open(myFilename, 'r+') as file:
        file.truncate(0)
    listoula = Lista()

    l = LinkedList()
    print('~'*5,"Linked List",'~'*5)
    #for i in range(1,32):
    listoula.add(1,1)
    #listoula.add(1,1)
    #for i in range (0,1000):
    #    c = random.randrange(0,2**18)
    #    d = random.randrange(0,2**18)
    #    l.append(c, d)
    #    listoula.add(c, d)
    a = random.randrange(0,2**18)
    b = random.randrange(0,2**18)
    print("Searching for random pair (%d,%d) in the linked list..." %(a, b))
    l.search(a, b)
    print("Comparisons:", comparisons)

    print('~'*5,"Hashtable",'~'*5)
    HT = HashTable()
    for i in range (0,1000):
        HT.insertKey(random.randrange(0,2**18), random.randrange(0,2**18))
    a = random.randrange(0,2**18)
    b = random.randrange(0,2**18)
    print("Searching for random pair (%d,%d) in the hashtable..." %(a, b))
    HT.searchNode(a, b)
    print("Comparisons:", comparisons)
        

if __name__ == "__main__":
    main()
