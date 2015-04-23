import json
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import  get_object_or_404, redirect, render
from django.utils import timezone
from helpers import make_quiz, make_tree_question
from models import Quiz, Question, QuestionInstance
from quiz_service.service import get_quizzes, get_exercise, get_result, get_question_type, QType
from time import strptime

# Create your views here.
# starting page
@login_required
def quizzes(request):
    # get all quizzes, will potentially modify to get quizzes for a user
    d = {
        'quizzes': get_quizzes(),
    }
    return render(request, 'quizzes/quizzes.html', d)

@login_required
def quiz(request, quiz_id):
    # get that quiz
    # NOTE: THIS IS CURRENTLY NOT FUNCTIONAL, NEED QUIZ SERVICE TO SUPPORT GETTING QUESTIONS OF QUIZ
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

@login_required
def question_test(request, quiz_id, question_idx):
    quiz_id = int(quiz_id)
    question_idx = int(question_idx)
    # connect to SOAP service
    if request.method == 'GET':
        # get the question and its type
        question = get_exercise('vi', quiz_id, question_idx)
        question_type = get_question_type(question)

        # parse the question
        # set up context for template
        d = {
            'question_type': question_type,
            'prompt':        question['prompt'],
            'seed':          question['seed'],
            'title':         question['title'],
        }
        if question_type == QType.BST_INSERT:
            d['promptPretty'] = question['promptPretty']
            d['structure']    = json.dumps(question['promptPrettyStructure'].split())
        elif question_type == QType.BST_SEARCH:
            d['promptPretty'] = question['promptPretty']
            d['structure']    = question['promptPrettyStructure']
        elif question_type == QType.CHECKBOX or question_type == QType.RADIO:
            d['statements'] = question['statements']

        # render the appropriate template
        if question_type == QType.BST_INSERT:
            return render(request, 'quizzes/question/insert_test.html', d)
        elif question_type == QType.BST_SEARCH:
            return render(request, 'quizzes/question/search_test.html', d)
        elif question_type == QType.SHORT_ANSWER:
            return render(request, 'quizzes/question/short_answer.html', d)
        elif question_type == QType.RADIO:
            return render(request, 'quizzes/question/radio.html', d)
        elif question_type == QType.CHECKBOX:
            return render(request, 'quizzes/question/checkbox.html', d)
        else:
            HttpResponse(400, 'sorry!')

    if request.method == 'POST':
        # get the type of the question
        question_type = request.POST.get('question_type')

        # read in the answer
        user_answer = request.POST.get('answer')
        if question_type == QType.BST_SEARCH:
            user_answer = json.loads(user_answer)
        elif question_type == QType.CHECKBOX:
            user_answer = " ".join(request.POST.getlist('answer'))

        # submit the answer and get the result
        result = get_result('vi', quiz_id, question_idx, user_answer)
        print(result)

        # parse the result
        # set up context for template
        d = {
            'user_answer':  user_answer,
            'correct':      result['score'] == result['maxScore'],
            'answer':       result['answer'],
            'max_score':    result['maxScore'],
            'score':        result['score'],
            'seed':         result['seed'],
            'title':        result['title'],
            'prompt':       result['prompt'],
            'quiz_id':      quiz_id,
            'question_idx': question_idx,
        }
        if 'explanation' in result:
            d['explanation'] = result['explanation']
        if question_type == QType.BST_INSERT:
            d['answer']       = json.loads(result['explanationPrettyStructure'])[-1]
            d['promptPretty'] = result['promptPretty']
            d['structure']    = result['promptPrettyStructure']
        elif question_type == QType.BST_SEARCH:
            d['promptPretty'] = result['promptPretty']
            d['structure'] = result['promptPrettyStructure']
        elif question_type == QType.RADIO:
            d['statements']     = result['statements']
            d['answer']      = int(result['answer'])
            d['user_answer'] = int(user_answer)
        elif question_type == QType.CHECKBOX:
            d['explanations']   = result['explanations']
            d['statements']     = result['statements']
            d['statements_and_explanations'] = zip(result['statements'], result['explanations'])
            d['answer']      = [int(a) for a in result['answer'].split()]
            d['user_answer'] = [int(a) for a in user_answer.split()]

        # render the appropriate template
        if question_type == QType.BST_INSERT:
            return render(request, 'quizzes/answer/insert_test.html', d)
        elif question_type == QType.BST_SEARCH:
            return render(request, 'quizzes/answer/search_test.html', d)
        elif question_type == QType.SHORT_ANSWER:
            return render(request, 'quizzes/answer/short_answer.html', d)
        elif question_type == QType.RADIO:
            return render(request, 'quizzes/answer/radio.html', d)
        elif question_type == QType.CHECKBOX:
            return render(request, 'quizzes/answer/checkbox.html', d)
        else:
            HttpResponse(400, 'sorry!')



# get questions and post answers
@login_required
def question(request, quiz_id, question_idx, instance_idx):
    quiz_id = int(quiz_id)
    question_idx = int(question_idx)
    instance_idx = int(instance_idx)

    quiz = get_object_or_404(Quiz, pk=quiz_id)

    question_queryset = Question.objects.filter(quiz__id=quiz.id, idx=question_idx)
    question = instance = None
    if len(question_queryset) == 0:
        raise Http404('Question not found')
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
            return HttpResponse(400) # bad operation
        else:
            instance = instance_queryset[0]

        d = {
            'quiz': quiz,
            'question': question,
            'instance': instance,
        }

        if question.q_type == 'insert':
            if instance.complete or timezone.now() > instance.end_time:
                return render(request, 'quizzes/answer/insert.html', d)
            else:
                return render(request, 'quizzes/question/insert.html', d)
        elif question.q_type == 'search':
            if instance.complete or timezone.now() > instance.end_time:
                return render(request, 'quizzes/answer/search.html', d)
            else:
                return render(request, 'quizzes/question/search.html', d)

    else:
        if len(instance_queryset) == 0:
            raise Http404('QuestionInstance not found.')
        else:
            instance = instance_queryset[0]

        # if it hasn't been too long and hasn't been answered already
        if timezone.now() < instance.end_time and not instance.complete:
            # POST - user is answering question
            user_answer = request.POST.get('answer')
            if user_answer != [] and not user_answer:
                user_answer = json.dumps('')
            user_answer = json.loads(user_answer)
            # deserialize answer
            answer = json.loads(instance.answer)

            # check correctness, assign complete, assign score
            instance.user_answer = json.dumps(user_answer)
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

        if question.q_type == 'insert':
            return render(request, 'quizzes/answer/insert.html', d)
        elif question.q_type == 'search':
            return render(request, 'quizzes/answer/search.html', d)





