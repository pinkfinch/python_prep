def print_backward(node):

    def recurse(node):
        if not node:
            return
        recurse(node.next)
        print(node.value)
    recurse(node)

def swap(head, a, b):
    prev_a,prev_b = None, None
    curr_a, curr_b = None, None
    prev = None
    current = head
    while current:
        if current.value == a:
            prev_a = prev
            curr_a = current
        elif current.value == b:
            prev_b = prev
            curr_b = current
        prev = current
        current = current.next
        if curr_a and curr_b: break

    if curr_a and curr_b:
        tmp = curr_a.next
        curr_a.next = curr_b.next
        curr_b.next = tmp
    if prev_a:
        prev_a.next = curr_b
    if prev_b:
        prev_b.next = curr_a

class ListNode:
    def __init__(self, value=None):
        self.value = value
        self.next = None

def generate_list(lst):
    if len(lst) == 0:
        return None
    head = ListNode(lst[0])
    current = head
    for i in range(1, len(lst)):
        current.next = ListNode(lst[i])
        current = current.next
    return head



print_backward(generate_list([1,3,5,7]))
li = [5,1,7,10]
swap(generate_list(li), 5,1)
print(li)
