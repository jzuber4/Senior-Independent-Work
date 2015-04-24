import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, HttpResponse
from django.shortcuts import  get_object_or_404, redirect, render
from django.utils import timezone
from quiz_service import service as qs
from quiz_service.service import QType, get_question_type
from time import strptime

# Create your views here.
# starting page
@login_required
def quizzes(request):
    # get all quizzes, will potentially modify to get quizzes for a user
    d = {
        'quizzes': qs.get_quizzes(),
    }
    return render(request, 'quizzes/quizzes.html', d)

@login_required
def quiz(request, quiz_id):
    # get that quiz
    # NOTE: THIS IS CURRENTLY NOT FUNCTIONAL, NEED QUIZ SERVICE TO SUPPORT GETTING QUESTIONS OF QUIZ
    qs.select_quiz(request.user.username, quiz_id)
    return render (request, 'quizzes/quiz.html')

@login_required
def question(request, quiz_id, question_idx):
    quiz_id = int(quiz_id)
    question_idx = int(question_idx)
    # connect to SOAP service
    if request.method == 'GET':
        # get the question and its type
        question = qs.get_exercise(request.user.username, quiz_id, question_idx)
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
            # need array of elements to insert, given whitespace separated string
            d['structure']    = json.dumps(question['promptPrettyStructure'].split())
        elif question_type == QType.BST_SEARCH:
            d['promptPretty'] = question['promptPretty']
            d['structure']    = question['promptPrettyStructure']
        elif question_type == QType.CHECKBOX:
            d['statements'] = question['statements']
        elif question_type == QType.MATCHING:
            d['options']    = question['options']
            d['statements'] = question['statements']
        elif question_type == QType.RADIO:
            d['statements'] = question['statements']

        # render the appropriate template
        if question_type == QType.BST_INSERT:
            return render(request, 'quizzes/question/insert.html', d)
        elif question_type == QType.BST_SEARCH:
            return render(request, 'quizzes/question/search.html', d)
        elif question_type == QType.CHECKBOX:
            return render(request, 'quizzes/question/checkbox.html', d)
        elif question_type == QType.MATCHING:
            return render(request, 'quizzes/question/matching.html', d)
        elif question_type == QType.RADIO:
            return render(request, 'quizzes/question/radio.html', d)
        elif question_type == QType.SHORT_ANSWER:
            return render(request, 'quizzes/question/short_answer.html', d)
        else:
            return HttpResponse(400, 'Sorry, that question type is not supported.')

    if request.method == 'POST':
        # get the type of the question
        question_type = request.POST.get('question_type')

        # read in the answer
        user_answer = request.POST.get('answer')
        if question_type == QType.BST_SEARCH:
            user_answer = json.loads(user_answer)
        elif question_type == QType.CHECKBOX or question_type == QType.MATCHING:
            user_answer = " ".join(request.POST.getlist('answer'))

        # submit the answer and get the result
        result = qs.get_result(request.user.username, quiz_id, question_idx, user_answer)
        question_type = get_question_type(result)

        # parse the result
        # set up context for template
        d = {
            'answer':       result['answer'],
            'correct':      result['score'] == result['maxScore'],
            'max_score':    result['maxScore'],
            'prompt':       result['prompt'],
            'question_idx': question_idx,
            'quiz_id':      quiz_id,
            'score':        result['score'],
            'seed':         result['seed'],
            'title':        result['title'],
            'user_answer':  user_answer,
        }
        if 'explanation' in result:
            d['explanation'] = result['explanation']
        if question_type == QType.BST_INSERT:
            # explanationPrettyStructure is a list of trees as keys are inserted
            # the last tree in the list is the final state
            d['answer']       = json.loads(result['explanationPrettyStructure'])[-1]
            d['promptPretty'] = result['promptPretty']
            d['structure']    = result['promptPrettyStructure']
        elif question_type == QType.BST_SEARCH:
            d['promptPretty'] = result['promptPretty']
            d['structure']    = result['promptPrettyStructure']
        elif question_type == QType.CHECKBOX:
            d['explanations'] = result['explanations']
            d['statements']   = result['statements']
            d['statements_and_explanations'] = zip(result['statements'], result['explanations'])
            # get array of ints from whitespace separated string
            d['answer']      = [int(a) for a in result['answer'].split()]
            d['user_answer'] = [int(a) for a in user_answer.split()]
        elif question_type == QType.MATCHING:
            d['options'] = result['options']
            # put all info in list of tuples for easy iteration
            e = json.loads(result['explanations'])
            s = result['statements']
            a = [d['options'][int(a)] for a in result['answer'].split()]
            u = [d['options'][int(u)] for u in user_answer.split()]
            d['info'] = [(s[i], u[i], a[i], e[i]) for i in range(len(s))]
        elif question_type == QType.RADIO:
            d['statements']  = result['statements']
            d['answer']      = int(result['answer'])
            d['user_answer'] = int(user_answer)

        # render the appropriate template
        if question_type == QType.BST_INSERT:
            return render(request, 'quizzes/answer/insert.html', d)
        elif question_type == QType.BST_SEARCH:
            return render(request, 'quizzes/answer/search.html', d)
        elif question_type == QType.CHECKBOX:
            return render(request, 'quizzes/answer/checkbox.html', d)
        elif question_type == QType.MATCHING:
            return render(request, 'quizzes/answer/matching.html', d)
        elif question_type == QType.RADIO:
            return render(request, 'quizzes/answer/radio.html', d)
        elif question_type == QType.SHORT_ANSWER:
            return render(request, 'quizzes/answer/short_answer.html', d)
        else:
            return HttpResponse(400, 'Sorry, that question type is not supported.')

@login_required
@user_passes_test(lambda u: u.userinfo.is_teacher)
def create_quiz(request):
    if request.method == 'GET':
        question_types_and_titles = qs.get_question_types()
        question_types = [t[0] for t in question_types_and_titles]
        question_titles = [t[1] for t in question_types_and_titles]
        d = {
            'question_titles': json.dumps(question_titles),
            'question_types': json.dumps(question_types),
            'grading_types': qs.get_grading_types(),
        }
        return render(request, 'quizzes/create_quiz.html', d)
    else:
        pass








