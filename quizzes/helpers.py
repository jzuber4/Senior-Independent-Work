import datetime
import json
from django.utils import timezone
from quizzes.models import Quiz, Question, QuestionInstance
from random import randint

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

# define normal compare function
def compare(a, b):
    if a < b:
        return -1
    elif a == b:
        return 0
    else:
        return 1

# make a quiz and 5 random questions, save all of it to the db and return
def make_quiz():
    quiz = Quiz(name="This is the name of the quiz", num_questions=5, status="in progress", max_score=50.0)
    quiz.save()
    for i in range(5):
        q_type = random_question_type()
        Question(q_type=q_type, quiz=quiz, idx=i).save()
    return quiz

def random_question_type():
    N = 2
    roll = randint(0,N)
    if roll == 0:
        return "search"
    else:
        return "insert"

def make_tree_question(question, idx):
    # only search questions so far
    if question.q_type == "search":
        return make_search_question(question, idx)
    elif question.q_type == "insert":
        return make_insert_question(question, idx)
    else:
        raise ValueError("question.q_type is invalid value: {}".format(question.q_type))

def make_insert_question(question, idx):
    # range of integers
    lo = 0
    hi = 100
    # number of nodes
    N = 10

    # numbers to insert
    numbers = []
    for _ in range(N):
        choice = randint(lo, hi)
        while choice in numbers:
            choice = randint(lo, hi)
        numbers.append(choice)

    # make the prompt
    prompt = "Given the numbers {0}, click on empty nodes to insert them in the tree.".format(numbers[1:])

    root = BNode(numbers[0])
    for num in numbers[1:]:
        root.insert(num, compare)

    answer = json.dumps(root.to_serializable())
    structure = json.dumps(numbers)

    # create model
    end_time = timezone.now() + datetime.timedelta(hours=1)
    instance = QuestionInstance(prompt=prompt, end_time=end_time,
                                structure=structure, answer=answer,
                                idx=idx, question=question)
    instance.save()
    return instance


def make_search_question(question, idx):
    # range of integers
    lo = 0
    hi = 100
    # number of nodes
    N = 20

    # choose number to be searched for
    choice = randint(lo, hi)

    # make the prompt
    prompt = "Given the following BST, suppose that you search for the key {0}. What is the sequence of keys in the BST that are compared to {0}?".format(choice)

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
    end_time = timezone.now() + datetime.timedelta(hours=1)
    instance = QuestionInstance(prompt=prompt, end_time=end_time,
                                structure=structure, answer=answer,
                                idx=idx, question=question)
    instance.save()
    return instance



