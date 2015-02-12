from trees.models import Question
from random import randint
import json

# binary tree
class BNode:
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
                self.left = BNode(item)
            else:
                self.left.insert(item, compare)
        else:
            if self.right is None:
                self.right = BNode(item)
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

    def to_serializable(self):
        children = []

        # recursively make left subtree
        if not self.left is None:
            children.append(self.left.to_serializable())
        else:
            # create fake leaf node so every node has 2 children
            children.append({'name': None, 'children': []})

        # recursively make right subtree
        if not self.right is None:
            children.append(self.right.to_serializable())
        else:
            # create fake leaf node so every node has 2 children
            children.append({'name': None, 'children': []})

        return {'name': self.item, 'children': children}


def make_tree_question():
    # only search questions so far
    return make_search_question()

def make_insert_question():
    # range of integers
    lo = 0
    hi = 100
    # number of nodes
    N = 10

    # make list of random integers and tree made from inserting them
    first = randint(lo, hi)
    sequence = [first]
    root = BNode(first)
    for _ in range(N - 1):
        num = randint(lo,hi)
        root.insert(num, compare)
        sequence.append(num)

    # make the prompt
    prompt = "Starting from an empty BST, suppose that you insert the sequence of keys: {0}."
    + " What is the level order traversal of the final tree? Click on blank nodes to insert"
    + " keys at that node, or type in the level order traversal."
    prompt = prompt.format(sequence)

    # serialize to json
    answer = json.dumps(root.to_serializable())
    structure = json.dumps(sequence)

    # create model
    q_type = Question.BSTSEARCH
    question = Question(q_type=q_type, prompt=prompt,
                        structure=structure, answer=answer)
    return question

def make_search_question():
    # range of integers
    lo = 0
    hi = 100
    # number of nodes
    N = 20

    # choose number to be searched for
    choice = randint(lo, hi)

    # make the prompt
    prompt = "Given the following BST, suppose that you search for the key {0}. What is the sequence of keys in the BST that are compared to {0}?".format(choice)

    # define normal compare function
    def compare(a, b):
        if a < b:
            return -1
        elif a == b:
            return 0
        else:
            return 1

    # make the tree
    root = BNode(randint(lo, hi))
    for _ in range(N - 1):
        root.insert(randint(lo,hi), compare)

    # define compare function that tracks the items compared against
    c = []
    def compare_with_side_effect(a, b):
        c.append(b)
        return compare(a, b)

    # fill c with answer
    root.search(choice, compare_with_side_effect)

    # serialize to json
    structure = json.dumps(root.to_serializable())
    answer = json.dumps(c)

    # create model
    q_type = Question.BSTSEARCH
    question = Question(q_type=q_type, prompt=prompt,
                        structure=structure, answer=answer)
    return question



