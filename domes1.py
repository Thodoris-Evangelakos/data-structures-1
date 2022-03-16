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
            print("(", self.head.data_x,",", self.head.data_y,")")
            self.head = self.head.next
        self.head = self.firstHead #pointer reset

#search function that goes through each node, comparing the x and y values

    def search(self, user_x, user_y):
        print("Searching for","(",user_x,",",user_y,")")
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
        print("Total searches:", searches+1)
            

l = LinkedList()
l.append(5,12)
l.append(10,42)
l.append(19,28)
l.search(10,42)
l.printList()
print("Linked list size:",l.count)
 
