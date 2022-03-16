# -*- coding: cp1253 -*-


from random import seed
from random import randint
import numpy as np


#Ν=2^18, Μ=500
M = 10
N = 101


seed(0)
class Node:
    def __init__(self, data_x, data_y):
        self.data_x = data_x
        self.data_y = data_y
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.firstHead = None
        self.tail = None
        self.count = 0

    def append(self, data_x, data_y):
        node = Node(data_x,data_y)

        if not self.head:
            self.head = node
            self.firstHead = node #permanently stores the first node, or at least I fucking hope so :)
        else:
            self.tail.next = node

        self.tail = node
        self.count += 1

# Complete the printLinkedList function below.

    def printList(self):
        if not self.head:
            print(None)
        while self.head:
            if self.head.next:
                print("(%d,%d)" %(self.head.data_x, self.head.data_y),"--->",end="  ")
            else:
                print("(%d,%d)" %(self.head.data_x,self.head.data_y))
            self.head = self.head.next
        self.head = self.firstHead #pointer reset



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
        while self.head is not None:
            if self.head.data_x == user_x and self.head.data_y == user_y:
                found = 1
                break
            searches += 1
            self.head = self.head.next
        self.head = self.firstHead #pointer reset
        if bool(found):
            print("Found!")
        else:
            print("Not found :(")
        print("Total searches: %d" %(searches+1))
            

class HashTable():
    def __init__(self):
        self.hashtable = np.array([None]*N)
        for x in range(M):
            self.hashtable[x] = LinkedList()

    def getHash(self, x, y):
        H = (x*N + y)%M
        #print("H(%d,%d) = %d" %(x, y ,H))
        return H

    def insertKey(self, x, y):
        index = self.getHash(x, y)
        self.hashtable[index].append(x, y)

    def searchKey(self, x, y):
        print("Searching HashTable for the index of (%d,%d)" %(x,y))
        index = self.getHash(x,y)
        boolean = self.hashtable[index]
        return boolean

    def searchNode(self, x, y):
        index = self.getHash(x,y)
        print("Index of (%d,%d): %d" %(x, y, self.getHash(x, y)))
        print("Searching at given index...")
        self.hashtable[index].search(x,y)
    
    def printHashTable(self):
        print("Hash table is :- \n")
        print("Index \t\tValues\n")
        for x in range(M) :
            print(x,end ="\t\t")
            self.hashtable[x].printList()
    
########### LINKED LIST TESTING ##############
print("~~~~~Linked List Testing~~~~~\n\n\n")
l = LinkedList()

l.append(5,12)
l.append(10,42)
l.append(19,28)

l.search(10,42)

print("~~searching for random int~~")
l.search(randint(0,100),randint(0,100))
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
