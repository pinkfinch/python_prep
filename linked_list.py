# Create a method which prints value of each node till the tail in a linked list

# Input node: ListNode
# Example: {1}->{5}->{7}->10->null
# Prints  1
#         5
#         7
#         10

class ListNode:

    def __init__(self, value, next=None):
        self.value = value
        self.next = next

def printForward(node):
    if node is None: return
    current = node
    while current:
        print(current.value)
        current = current.next

def printBackward(node):
    if node is None: return
    current = node
    arr = []
    while current:
        arr.append(current.value)
        current = current.next
    arr.reverse()
    print(arr)

def printBackwardRecurse(node):

    def traverse(node):
        if node is None: return
        traverse(node.next)
        print(node.value)
    traverse(node)


def reverseLinkedList(node):
    if node is None: return
    current = node
    prev = None
    nxt = None
    while current:
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt
    return prev

#create a method that swaps the first occurence of locations of two nodes in linked list
#
# example swap(head, 5,10)
# {1}->{5}->{7}->{10}

# will return
# {1}->{10}->{7}->{5}
def swapListNodes(head, a, b):
    a_pos, b_pos = None, None
    current = head
    while current:
        if current.value == a:
            a_pos = current
        if current.value == b:
            b_pos = current
        if a_pos is not None and b_pos is not None:
            a_pos.value, b_pos.value = b_pos.value, a_pos.value
            return head
        current = current.next
    return head

def swapListNodesPointers(head, a, b):
    a_pos, b_pos = None, None
    a_prev, b_prev = None, None
    ph = ListNode(-1)
    ph.next = head
    current = ph
    prev = head
    while current:
        if current.value == a:
            a_pos = current
            prev = a_prev
        if current.value == b:
            b_pos = current
            prev = b_prev
        if a_pos is not None and b_pos is not None:
            tmp = a_pos.next
            a_pos.next = b_pos.next
            b_pos.next = tmp
            if a_prev is None:
                head = b_pos
            tmp = b_pos
            if a_prev: a_prev.next = b_pos
            if b_prev: b_prev.next = a_pos
            break
        prev = current
        current = current.next
    return  head

def createLL(arr):
    if len(arr) == 0: return None
    head = ListNode(arr[0])
    current = head
    for i in range(1,len(arr)):
        next_node = ListNode(arr[i])
        current.next = next_node
        current = next_node

    return head

node = createLL([1,24,55,6,8,9])
printForward(node)
printBackward(node)
print("recursively print reversed linked list:")
printBackwardRecurse(node)
reversed_head = reverseLinkedList(node)
print("reversed linked list:")
printForward(reversed_head)
print("swap list:")
swapListNodes(reversed_head, 24, 8)
printForward(reversed_head)

print("swapping pointers")
swapListNodesPointers(reversed_head, 9, 8)
printForward(reversed_head)
