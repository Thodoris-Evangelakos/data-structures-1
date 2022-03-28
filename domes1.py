#imports
import random
import numpy as np
import operator


#Ν=2^18, Μ=500
M = 10
N = 101

#LL code either belongs to codersalgo (https://codersalgo.com/separate-chaining-in-python/) or the GeeksForGeeks lads
class Node: #node class, holds 2 variables
    def __init__(self, data_x, data_y):
        self.data_x = data_x
        self.data_y = data_y
        self.next = None

class LinkedList: #linked list class, stores the head, the first node of the linked list, the tail and a count (used in everything associated with length)
    def __init__(self):
        self.head = None
        self.firstHead = None
        self.tail = None
        self.count = 0

    def append(self, data_x, data_y):
        node = Node(data_x,data_y)

        if not self.head: #checks if the LL is empty. If it is, it creates a node at the head
            self.head = node #creates a node at the start
            self.firstHead = node #stores the first node
        else:
            self.tail.next = node #if nodes are present, creates a node after the tail

        self.tail = node #updates the tail
        self.count += 1 #increments the length of the LL by 1

    def printList(self): #prints the LL
        if not self.head: #if self.head is NULL, prints None
            print(None)
        while self.head: #iterates through nodes until the head is null
            if self.head.next: #checks if there is a node linked to the current one, purely for formatting
                print("(%d,%d)" %(self.head.data_x, self.head.data_y),"--->",end="  ")
            else:
                print("(%d,%d)" %(self.head.data_x,self.head.data_y))
            self.head = self.head.next #goes to the next node
        self.head = self.firstHead #pointer reset

    def getListContents(self): #shoves all the data in a List
        bytesFromList = []
        while self.head: #much like the printList method, it goes through the list, appending her contents into a List
            bytesFromList.append(self.head.data_x)
            bytesFromList.append(self.head.data_y)
            self.head = self.head.next
        self.head = self.firstHead #pointer reset
        return bytesFromList


#Old and depracated printList function, the one above helps better visualize data

    #def printList(self):
        #print("~~~~Printing the entire linked list~~~~")
        #while self.head is not None:
            #print("(%d,%d)" %(self.head.data_x,self.head.data_y))
            #self.head = self.head.next
        #self.head = self.firstHead #pointer reset

#search function that goes through each node, comparing the x and y values

    def search(self, user_x, user_y):
        print("Searching for (%d,%d)" %(user_x ,user_y,))
        searches = 0
        found = 0
        while self.head is not None: #while we're at the last node or earlier
            if self.head.data_x == user_x and self.head.data_y == user_y:
                found = 1 #flips the found switch
                break #breaks out of the while loop
            searches += 1
            self.head = self.head.next #goes to the next head
        self.head = self.firstHead #pointer reset
        if bool(found): #switch check
            print("Found!")
        else:
            print("Not found :(")
        print("Total searches: %d" %(searches+1))
        return found 

#hashtable IP belongs to codersalgo, https://codersalgo.com/separate-chaining-in-python/

class HashTable():
    def __init__(self):
        self.hashtable = np.array([None]*N) #creates an array of size N
        for x in range(M):
            self.hashtable[x] = LinkedList() #creates a LL at every index of the hashtable

    def getHash(self, x, y): #calculates the Hash
        H = (x*N + y)%M
        #print("H(%d,%d) = %d" %(x, y ,H))
        return H

    def insertKey(self, x, y): #adds a key using the hash as an index and the append function (or method) of the LL
        index = self.getHash(x, y)
        self.hashtable[index].append(x, y)

    def searchKey(self, x, y): #searches for a certain x,y pair
        print("Searching HashTable for the index of (%d,%d)" %(x,y))
        index = self.getHash(x,y) #gets the index from the given pair
        boolean = self.hashtable[index].search(x, y) #looks if that key exists in the hashtable
        return boolean #returns wether the key was found or not

#should merge searchNode with searchKey, not sure why I made 2 separate functions, they do the same thing

    def searchNode(self, x, y):
        index = self.getHash(x,y)
        print("Index of (%d,%d): %d" %(x, y, self.getHash(x, y)))
        print("Searching at given index...")
        self.hashtable[index].search(x,y)
 
 #prints the entire hashTable
    
    def printHashTable(self):
        print("Hash table is :- \n")
        print("Index \t\tValues\n")
        for x in range(M) :
            print(x,end ="\t\t")
            self.hashtable[x].printList()

#writing stuff to the disk

def displayBytes(bytes):
    print("-"*20)
    for index, item in enumerate(bytes):
        print(f'{index} = {item} ({hex(item)})')
    print("-"*20)

#Write bytes

def writeBytes(filename, bytes):
    with open(filename, 'wb') as file:
        for i in bytes:
            file.write(i.to_bytes(1, byteorder='big'))

#Read bytes

def readBytes(filename):
    bytes = []
    with open(filename, 'rb') as file:
        while True:
            b = file.read(1)
            if not b:
                break
            bytes.append(int.from_bytes(b, byteorder='big'))
    return bytes



########### LINKED LIST TESTING ##############
print("~~~~~Linked List Testing~~~~~\n\n\n")
l = LinkedList()

l.append(5,12)
l.append(10,42)
l.append(19,28)

l.search(10,42)

print("~~searching for random int~~")
l.search(random.randint(0,100),random.randint(0,100))
l.printList()
print("Linked list size: %d" %(l.count))
print("\n\n")
###########  HASHTABLE TESTING ###############
print("~~~~~Hashtable testing~~~~~\n\n\n")
HT = HashTable()
HT.insertKey(10, 50)
HT.insertKey(90, 45)
HT.insertKey(25, 18)
HT.insertKey(5, 19)
HT.insertKey(35, 55)
HT.insertKey(27, 2)
HT.insertKey(14, 88)
HT.insertKey(15, 89)

if HT.searchKey(14, 88):
    print("Found the key!")
else:
    print("Key wasn't found :(")

#search Nodes

HT.printHashTable()
HT.searchNode(15, 89)

#write stuff to the disk
print("~~~~~Disk-stuff testing~~~~~\n\n\n")
outBytes = l.getListContents()
displayBytes(outBytes)

filename = 'byteTest.bin'
writeBytes(filename, outBytes)

inBytes = readBytes(filename) #reads the bytes that were written in the file, that were originally in the linked list
displayBytes(inBytes)
print(f'Match: {operator.eq(outBytes, inBytes)}')
