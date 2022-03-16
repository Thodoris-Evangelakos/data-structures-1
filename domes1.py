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
        print("~~~~Printing the entire linked list~~~~")
        while self.head is not None:
            print("(%d,%d)" %(self.head.data_x,self.head.data_y))
            self.head = self.head.next
        self.head = self.firstHead #pointer reset

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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hashtable = np.array([None]*N)
        for x in range(N):
            self.hashtable[x] = LinkedList()

    def getHash(x, y):
        H = (x*N + y)%M
        print("H(%d,%d) = %d" %(x, y ,H))
        return H

    def insertKey(self, x, y):
        index = self.getHash(x, y)
        self.hashtable[index].append(x, y)

    def searchKey(self, x, y):
        index = self.getHash(x, y)
        boolean = self.hashtable[index]
        return boolean
    


l = LinkedList()
l.append(5,12)
l.append(10,42)
l.append(19,28)
l.search(10,42)
print("~~searching for random int~~")
l.search(randint(0,100),randint(0,100))
l.printList()
print("Linked list size: %d" %(l.count))
