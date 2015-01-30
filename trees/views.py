import json
from django.shortcuts import render, get_object_or_404
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
        else:
            # find from database, 404 if not present
            question = get_object_or_404(Question, pk=pk)

        d = {
            'pk': pk,
            'prompt': question.prompt,
            'structure': question.structure
        }

        return render(request, 'trees/question.html', d)
    else:
        # POST - user is answering question
        user_answer = request.POST.get('answer')

        d = {}
        if not user_answer is None:
            try:
                user_answer = [int(s.strip()) for s in user_answer.split(',')]
            except ValueError:
                d['message'] = 'Invalid input, needs to be a string of integers separated by commas.'
                d['success'] = False
                d['error'] = True
                d['user_answer'] = user_answer
                return render(request, 'trees/answer.html', d)

            d['error'] = False

            # get corresponding question / answer
            question = get_object_or_404(Question, pk=pk)

            # deserialize answer
            answer = json.loads(question.answer)

            # test for equivalence of answers
            correct = len(user_answer) == len(answer)
            correct &= all((a == b for (a,b) in zip(user_answer, answer)))

            # save for template
            d['answer'] = answer
            d['user_answer'] = user_answer

            # return status
            if correct:
                d['message'] = 'Correct!'
                d['success'] = True
            else:
                d['message'] = 'Sorry, that was incorrect.'
                d['success'] = False
        else:
            d['message'] = 'No answer provided'
            d['success'] = False
            d['error'] = True


        return render(request, 'trees/answer.html', d)





