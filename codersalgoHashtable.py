#https://codersalgo.com/separate-chaining-in-python/


#hashtable with separate chaining


import numpy as np

#separate chaining in python
class Node() :
    
    def __init__(self,value) :
        self.value = value
        self.next = None

class Linked_List() :
    
    def __init__(self) :
        self.head = None
        
    def insert(self,value) :
        if not self.head :
            self.head = Node(value)
        else :
            temp = self.head
            while temp.next :
                temp = temp.next
            temp.next = Node(value)
            
    def search(self,value) :
        temp = self.head
        while temp :
            if temp.value == value :
                return True
            temp = temp.next
        return False
    
    def print_LL(self) :
        temp = self.head
        if not temp :
            print(None)
        while temp :
            if temp.next :
                print(temp.value,"--->",end ="  ")
            else :
                print(temp.value)
            temp = temp.next
            
            
class Hash_table() :
    def __init__(self,size) :
        self.size = size
        self.hashtable = np.array([None]*self.size)
        for x in range(self.size) :
            self.hashtable[x] = Linked_List()
        
    def hash(self,key) :
        # Hash function is h(x) = x%10
        return key%10
    
    def insert_key(self,key) :
        index = self.hash(key)
        self.hashtable[index].insert(key)
        
    def search_key(self,key) :
        index = self.hash(key)
        boolean = self.hashtable[index].search(key)
        return boolean
    
    def print_HT(self) :
        print("Hash table is :- \n")
        print("Index \t\tValues\n")
        for x in range(self.size) :
            print(x,end ="\t\t")
            self.hashtable[x].print_LL()
    
HT = Hash_table(10)
HT.insert_key(10)
HT.insert_key(90)
HT.insert_key(25)
HT.insert_key(5)
HT.insert_key(35)
HT.insert_key(27)
HT.insert_key(17)
HT.insert_key(22)
if HT.search_key(17) :
    print("Given key is present\n")
else :
    print("Given key is not present\n")
HT.print_HT()
