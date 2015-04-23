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
def question(request, quiz_id, question_idx):
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
            return render(request, 'quizzes/question/insert.html', d)
        elif question_type == QType.BST_SEARCH:
            return render(request, 'quizzes/question/search.html', d)
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
            return render(request, 'quizzes/answer/insert.html', d)
        elif question_type == QType.BST_SEARCH:
            return render(request, 'quizzes/answer/search.html', d)
        elif question_type == QType.SHORT_ANSWER:
            return render(request, 'quizzes/answer/short_answer.html', d)
        elif question_type == QType.RADIO:
            return render(request, 'quizzes/answer/radio.html', d)
        elif question_type == QType.CHECKBOX:
            return render(request, 'quizzes/answer/checkbox.html', d)
        else:
            HttpResponse(400, 'sorry!')





