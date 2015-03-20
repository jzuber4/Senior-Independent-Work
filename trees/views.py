import json
from django.core.urlresolvers import reverse
from django.shortcuts import  get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from models import Question
from helpers import make_tree_question

# Create your views here.
# starting page
@require_http_methods(['GET'])
def index(request):
    return render(request, 'trees/index.html')

# get questions and post answers
@require_http_methods(['GET', 'POST'])
def question(request, pk=None):
    if request.method == 'GET':
        # GET - user is asking for a question
        question = None

        # get question or generate new question
        if pk is None:
            # make new question and add it to the database
            question = make_tree_question()
            question.save()
            pk = question.pk
            return redirect(reverse('trees.views.question', args=[pk]))
        else:
            # find from database, 404 if not present
            question = get_object_or_404(Question, pk=pk)

        d = {
            'pk': pk,
            'type': question.q_type,
            'prompt': question.prompt,
            'structure': question.structure
        }

        if question.q_type == "insert":
            return render(request, 'trees/questionInsert.html', d)
        elif question.q_type == "search":
            return render(request, 'trees/questionSearch.html', d)

    else:
        # POST - user is answering question
        user_answer = request.POST.get('answer')
        if user_answer != [] and not user_answer:
            user_answer = json.dumps("")
        user_answer = json.loads(user_answer)

        # get corresponding question / answer
        question = get_object_or_404(Question, pk=pk)
        # deserialize answer
        answer = json.loads(question.answer)

        # save for template
        d = {}
        d['user_answer'] = json.dumps(user_answer)
        d['answer'] = question.answer
        d['structure'] = question.structure
        d['type'] = question.q_type

        # return status
        if answer == user_answer:
            d['message'] = 'Correct!'
            d['success'] = True
        else:
            d['message'] = 'Sorry, that was incorrect.'
            d['success'] = False

        if question.q_type == "insert":
            return render(request, 'trees/answerInsert.html', d)
        elif question.q_type == "search":
            return render(request, 'trees/answerSearch.html', d)





