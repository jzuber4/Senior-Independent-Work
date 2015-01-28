from models import Question

class Node:
    def __init__(self, item):
        self.left = None
        self.right = None
        self.item = item

    def insert(self, item, compare):
        comp = compare(item, self.item)
        if comp == 0:
            return
        elif comp < 0:
            if self.left is None:
                self.left = Node(item)
            else:
                self.left.insert(item, compare)
        else:
            if self.right is None:
                self.right = Node(item)
            else:
                self.right.insert(item, compare)

    def search(self, item, compare):
        comp = compare(item, self.item)
        if comp == 0:
            return self.item
        elif comp < 0:
            if self.left is None:
                return None
            else:
                return self.left.search(item, compare)
        else:
            if self.right is None:
                return None
            else:
                return self.right.search(item, compare)



def make_tree_question():
    # only search questions so far
    return make_search_question()

def make_search_question():
    # range of integers
    lo = 0
    hi = 100

    # choose number to be searched for
    choice = random.randint(lo, hi)

    # make the prompt
    prompt = "Given the following BST, suppose that you search for the key {0}. What is the sequence of keys in the BST that are compared to {0}." % choice

    # make the tree
    root = Node(random.randint(lo, hi))
    for _ in range(10):
        root.insert(Node(random.randint(lo,hi)))



    question = Question(prompt=prompt, structure=structure, answer=answer)



