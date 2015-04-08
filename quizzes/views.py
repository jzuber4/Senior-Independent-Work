import json
from django.core.urlresolvers import reverse
from django.shortcuts import  get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from models import Quiz, Question, QuestionInstance
from helpers import make_quiz, make_tree_question

# Create your views here.
# starting page
@require_http_methods(['GET'])
def quizzes(request):
    # get quizzes for a user
    # currently just gets all quizzes
    quizzes = Quiz.objects.all()
    # if I haven't made any quizzes yet
    if len(quizzes) < 10:
        quizzes = [make_quiz() for _ in range(10)]
    d = {
        'quizzes': quizzes,
    }
    return render(request, 'quizzes/quizzes.html', d)

@require_http_methods(['GET'])
def quiz(request, quizId):
    # get that quiz
    quiz = Quiz.objects.get(pk=quizId)
    questions = Question.objects.filter(quiz__id=quiz.id)
    questionInstances = QuestionInstance.objects.filter(question__id__in=[q.id for q in questions])
    sortedInstances = [[]] * len(questions)
    for qi in questionInstances:
        sortedInstances[qi.question.pk].append(qi)

    #for i in range(len(questions)):
    #    sortedInstances[i] = sorted(sortedInstances[i], key=lamba x: x.idx)
    d = {
        'quiz': quiz,
        'quizId': quizId,
        'questions': questions,
        'instances': sortedInstances,
    }
    return render (request, 'quizzes/quiz.html', d)

# get questions and post answers
@require_http_methods(['GET', 'POST'])
def question(request, quizId, questionIdx, instanceIdx):
    if request.method == 'GET':
        quiz = Quiz.objects.get(pk=quizId)
        question = Question.objects.filter(quiz__id=quiz.id, idx=questionIdx)
        instance = QuestionInstance.objects.filter(question__id=question.id, idx=instanceIdx)

        d = {
            'quizId': quizId,
            'questionIdx': questionIdx,
            'instanceIdx': instanceIdx,
            'type': question.q_type,
            'prompt': instance.prompt,
            'structure': instance.structure
        }

        if question.q_type == "insert":
            return render(request, 'quizzes/questionInsert.html', d)
        elif question.q_type == "search":
            return render(request, 'quizzes/questionSearch.html', d)

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
            return render(request, 'quizzes/answerInsert.html', d)
        elif question.q_type == "search":
            return render(request, 'quizzes/answerSearch.html', d)





