import json
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import  get_object_or_404, redirect, render
from django.utils import timezone
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
def quiz(request, quiz_id):
    # get that quiz
    quiz_id = int(quiz_id)
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(quiz__id=quiz.id)
    question_instances = QuestionInstance.objects.filter(question__id__in=[q.id for q in questions])
    sorted_instances = [[] for _ in questions]
    for qi in question_instances:
        sorted_instances[qi.question.idx].append(qi)
    for i in range(len(questions)):
        sorted_instances[i] = sorted(sorted_instances[i], key=lambda x: x.idx)
    questions_and_instances = [(questions[i], sorted_instances[i]) for i in range(len(questions))]
    d = {
        'quiz': quiz,
        'questions_and_instances': questions_and_instances,
    }
    return render (request, 'quizzes/quiz.html', d)

# get questions and post answers
@require_http_methods(['GET', 'POST'])
def question(request, quiz_id, question_idx, instance_idx):
    quiz_id = int(quiz_id)
    question_idx = int(question_idx)
    instance_idx = int(instance_idx)
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    question_queryset = Question.objects.filter(quiz__id=quiz.id, idx=question_idx)
    question = instance = None
    if len(question_queryset) == 0:
        raise Http404("Question not found")
    else:
        question = question_queryset[0]

    instance_queryset = QuestionInstance.objects.filter(question__id=question.id, idx=instance_idx)

    if request.method == 'GET':
        if len(instance_queryset) == 0 and question.attempts < question.max_attempts and instance_idx == question.attempts:
            instance = make_tree_question(question, instance_idx)
            question.attempts += 1
            question.in_progress = True
            question.save()
        elif instance_idx > question.attempts:
            print instance_idx, question.attempts
            return HttpResponse(400) # bad operation
        else:
            instance = instance_queryset[0]

        d = {
            'quiz': quiz,
            'question': question,
            'instance': instance,
        }

        if question.q_type == "insert":
            if instance.complete or timezone.now() > instance.end_time:
                return render(request, 'quizzes/answer/insert.html', d)
            else:
                return render(request, 'quizzes/question/insert.html', d)
        elif question.q_type == "search":
            if instance.complete or timezone.now() > instance.end_time:
                return render(request, 'quizzes/answer/search.html', d)
            else:
                return render(request, 'quizzes/question/search.html', d)

    else:
        if len(instance_queryset) == 0:
            raise Http404("QuestionInstance not found.")
        else:
            instance = instance_queryset[0]

        # if it hasn't been too long and hasn't been answered already
        if timezone.now() < instance.end_time and not instance.complete:
            # POST - user is answering question
            user_answer = request.POST.get('answer')
            if user_answer != [] and not user_answer:
                user_answer = json.dumps("")
            user_answer = json.loads(user_answer)
            # deserialize answer
            answer = json.loads(instance.answer)

            # check correctness, assign complete, assign score
            instance.user_answer = json.dumps(user_answer)
            print instance.user_answer
            instance.complete = True
            instance.correct = user_answer == answer
            # simple scoring function now
            instance.score = question.max_score if user_answer == answer else 0.0
            instance.save()
            # assign score to question
            # increase num_answered if applicable
            if instance.score > question.score:
                question.score = instance.score
                question.save()
                quiz.score = sum(q.score for q in Question.objects.filter(quiz__id=quiz.id))
                quiz.save()

        if not question.answered:
            question.answered = True
            quiz.num_answered += 1
            question.save()
            quiz.save()
        if question.in_progress:
            question.in_progress = False
            question.save()


        # save for template
        d = {
            'quiz': quiz,
            'question': question,
            'instance': instance,
        }

        if question.q_type == "insert":
            return render(request, 'quizzes/answer/insert.html', d)
        elif question.q_type == "search":
            return render(request, 'quizzes/answer/search.html', d)





