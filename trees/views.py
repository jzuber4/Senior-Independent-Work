from django.shortcuts import render
from helpers import make_tree_question

# Create your views here.
def index(request):
    # make new question and add it to the database
    new_question = make_tree_question()
    new_question.save()

    # present question to user
    id = new_question.id
    prompt = new_question.prompt
    structure = new_question.structure
    d = {"id": id, "prompt": prompt, "structure": structure}

    return render(request, "trees/index.html", d)

def question(request):
    pass
