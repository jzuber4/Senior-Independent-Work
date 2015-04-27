import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, HttpResponse
from django.shortcuts import  get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from models import Course, Quiz
from quiz_service import service as qs
from quiz_service.service import QuestionType, get_question_type
from time import strptime
from random import gauss

# Create your views here.
# starting page
@login_required
def courses(request):
    courses = qs.get_user_courses(request.user.username)
    courses = sorted(courses.items())
    d = {
        'courses': courses,
    }
    # update db info for courses
    for id, title in courses:
        course, created = Course.objects.get_or_create(service_id=id)
        if created or title != course.title:
            course.title = title
            course.save()
    # if user only has one course, might as well redirect to that
    if len(courses) == 1:
        course_id, _ = courses[0]
        return redirect('quizzes.views.course', course_id)
    return render(request, 'quizzes/courses.html', d)

@login_required
def course(request, course_id):
    course_id = int(course_id)

    # parse quizzes
    quizzes = []
    # quizzes come in id, json pairs
    for quiz_id, rest in sorted(qs.get_course_quizzes(request.user.username, course_id).items()):
        # decode the json into a dictionary
        quiz = json.loads(rest)
        # add the id back into the quiz
        quiz['quizId'] = quiz_id
        # parse the array of questions as json
        quiz['questions'] = [json.loads(q) for q in json.loads(quiz['questions'])]
        # precalculate the max score, it is not part of the quiz
        quiz['maxScore'] = sum(q['maxScore'] for q in quiz['questions'])
        quiz['startDate'] = parse_datetime(quiz['startDate'])
        quiz['endDate'] = parse_datetime(quiz['endDate'])
        quizzes.append(quiz)
        # save the title in the db
        quiz_model, created = Quiz.objects.get_or_create(service_id=quiz_id)
        if created or quiz["quizTitle"] != quiz_model.title:
            quiz_model.title = quiz["quizTitle"]
            quiz_model.save()

    d = {
        'course_id': course_id,
        # get the course title for display
        'course_title': Course.objects.get(service_id=course_id).title,
        'quizzes': quizzes,
    }

    return render(request, 'quizzes/course.html', d)

@login_required
def quiz(request, course_id, quiz_id):
    course_id = int(course_id)
    quiz_id   = int(quiz_id)

    # tell the service that the user is starting this quiz
    qs.select_quiz(request.user.username, quiz_id)

    quiz = qs.get_quiz_info(request.user.username, quiz_id)

    # questions represented as json array of json encoded questions
    quiz['questions'] = [json.loads(q) for q in json.loads(quiz['questions'])]
    quiz['maxScore'] = sum(q['maxScore'] for q in quiz['questions'])
    quiz['startDate'] = parse_datetime(quiz['startDate'])
    quiz['endDate'] = parse_datetime(quiz['endDate'])
    for q in quiz['questions']:
        q['attempts'] = sorted(json.loads(q['attempts']).items())

    # save title in db
    quiz_model, created = Quiz.objects.get_or_create(service_id=quiz_id)
    if created or quiz["quizTitle"] != quiz_model.title:
        quiz_model.title = quiz["quizTitle"]
        quiz_model.save()
    # load scores for quiz stats
    scores = qs.get_quiz_statistics(quiz['quizId'])
    d = {
        'course_id': course_id,
        'course_title': Course.objects.get(service_id=course_id).title,
        'quiz': quiz,
        'quiz_id': quiz['quizId'],
        'quiz_title': quiz['quizTitle'],
        'scores': json.dumps(scores),
    }
    d['mean'] = sum(scores) / len(scores)
    if len(scores) % 2 == 0:
        scores = sorted(scores)
        d['median'] = (scores[len(scores) / 2 - 1] + scores[len(scores) / 2]) / 2.0
    else:
        d['median'] = sorted(scores)[len(scores) / 2]

    return render (request, 'quizzes/quiz.html', d)

# render an attempt or a result
def render_attempt_or_result(request, course_id, quiz_id, question_idx, info, context={}):
    question_type = get_question_type(info)

    # set up context for template
    d = {
        'answer':        info['answer'], #TODO: answer not in CHECKBOX attempts
        'correct':       float(info['userScore']) == float(info['maxScore']),
        'course_id':     course_id,
        'course_title':  Course.objects.get(service_id=course_id).title,
        'max_score':     info['maxScore'],
        'prompt':        info['prompt'],
        'question_idx':  question_idx,
        'quiz_id':       quiz_id,
        'quiz_title':    Quiz.objects.get(service_id=quiz_id).title,
        'score':         info['userScore'],
        'seed':          info['seed'],
        'title':         info['title'],
        'user_answer':   info['userAnswer'],
        'attempts_left': info['leftAttempts'],
    }
    if 'explanation' in info:
        d['explanation'] = info['explanation']
    if question_type == QuestionType.BST_INSERT:
        # explanationPrettyStructure is a list of trees as keys are inserted
        # the last tree in the list is the final state
        d['answer']       = json.loads(info['explanationPrettyStructure'])[-1]
        d['promptPretty'] = info['promptPretty']
        d['structure']    = info['promptPrettyStructure']
    elif question_type == QuestionType.BST_SEARCH:
        d['promptPretty'] = info['promptPretty']
        d['structure']    = info['promptPrettyStructure']
    elif question_type == QuestionType.CHECKBOX:
        d['explanations'] = info['explanations']
        d['statements']   = info['statements']
        d['statements_and_explanations'] = zip(info['statements'], info['explanations'])
        # get array of ints from whitespace separated string
        d['answer']      = [int(a) for a in info['answer'].split()]
        d['user_answer'] = [int(a) for a in info['userAnswer'].split()]
    elif question_type == QuestionType.MATCHING:
        d['options'] = info['options']
        # put all info in list of tuples for easy iteration
        e = json.loads(info['explanations'])
        s = info['statements']
        a = [d['options'][int(a)] for a in info['answer'].split()]
        u = [d['options'][int(u)] for u in info['userAnswer'].split()]
        d['info'] = [(s[i], u[i], a[i], e[i]) for i in range(len(s))]
    elif question_type == QuestionType.RADIO:
        d['statements']  = info['statements']
        d['answer']      = int(info['answer'])
        d['user_answer'] = int(info['userAnswer'])

    # add extra context
    d.update(context)

    # render the appropriate template
    if question_type == QuestionType.BST_INSERT:
        return render(request, 'quizzes/answer/insert.html', d)
    elif question_type == QuestionType.BST_SEARCH:
        return render(request, 'quizzes/answer/search.html', d)
    elif question_type == QuestionType.CHECKBOX:
        return render(request, 'quizzes/answer/checkbox.html', d)
    elif question_type == QuestionType.MATCHING:
        return render(request, 'quizzes/answer/matching.html', d)
    elif question_type == QuestionType.NUMERIC:
        return render(request, 'quizzes/answer/numeric.html', d)
    elif question_type == QuestionType.RADIO:
        return render(request, 'quizzes/answer/radio.html', d)
    elif question_type == QuestionType.SHORT_ANSWER:
        return render(request, 'quizzes/answer/short_answer.html', d)
    else:
        return HttpResponse(400, 'Sorry, that question type is not supported.')

@login_required
def question(request, course_id, quiz_id, question_idx):
    course_id    = int(course_id)
    quiz_id      = int(quiz_id)
    question_idx = int(question_idx)
    # connect to SOAP service
    if request.method == 'GET':
        # get the question and its type
        question = qs.get_exercise(request.user.username, quiz_id, question_idx)
        question_type = get_question_type(question)

        # parse the question
        # set up context for template
        d = {
            'course_id':     course_id,
            'course_title':  Course.objects.get(service_id=course_id).title,
            'quiz_id':       quiz_id,
            'quiz_title':    Quiz.objects.get(service_id=quiz_id).title,
            'question_idx':  question_idx,
            'question_type': question_type,
            'prompt':        question['prompt'],
            'seed':          question['seed'],
            'title':         question['title'],
        }
        if question_type == QuestionType.BST_INSERT:
            d['promptPretty'] = question['promptPretty']
            # need array of elements to insert, given whitespace separated string
            d['structure']    = json.dumps(question['promptPrettyStructure'].split())
        elif question_type == QuestionType.BST_SEARCH:
            d['promptPretty'] = question['promptPretty']
            d['structure']    = question['promptPrettyStructure']
        elif question_type == QuestionType.CHECKBOX:
            d['statements'] = question['statements']
        elif question_type == QuestionType.MATCHING:
            d['options']    = question['options']
            d['statements'] = question['statements']
        elif question_type == QuestionType.RADIO:
            d['statements'] = question['statements']


        # render the appropriate template
        if question_type == QuestionType.BST_INSERT:
            return render(request, 'quizzes/question/insert.html', d)
        elif question_type == QuestionType.BST_SEARCH:
            return render(request, 'quizzes/question/search.html', d)
        elif question_type == QuestionType.CHECKBOX:
            return render(request, 'quizzes/question/checkbox.html', d)
        elif question_type == QuestionType.MATCHING:
            return render(request, 'quizzes/question/matching.html', d)
        elif question_type == QuestionType.NUMERIC:
            return render(request, 'quizzes/question/numeric.html', d)
        elif question_type == QuestionType.RADIO:
            return render(request, 'quizzes/question/radio.html', d)
        elif question_type == QuestionType.SHORT_ANSWER:
            return render(request, 'quizzes/question/short_answer.html', d)
        else:
            return HttpResponse(400, 'Sorry, that question type is not supported.')

    if request.method == 'POST':
        # get the type of the question
        question_type = request.POST.get('question_type')

        # read in the answer
        user_answer = request.POST.get('answer')
        if (len(user_answer) == 0):
            return redirect('quizzes.views.question', course_id, quiz_id, question_idx)
        if question_type == QuestionType.BST_SEARCH:
            user_answer = json.loads(user_answer)
        elif question_type == QuestionType.CHECKBOX or question_type == QuestionType.MATCHING:
            user_answer = " ".join(request.POST.getlist('answer'))

        # submit the answer and get the result
        result = qs.get_result(request.user.username, quiz_id, question_idx, user_answer)

        # render the correct page for this result
        return render_attempt_or_result(request, course_id, quiz_id, question_idx, result)

@login_required
def attempt(request, course_id, quiz_id, question_idx, attempt_idx):
    course_id    = int(course_id)
    quiz_id      = int(quiz_id)
    question_idx = int(question_idx)
    attempt_idx  = int(attempt_idx)

    # format attempt, place question and answers info in it
    attempt = qs.get_attempt_info(request.user.username, quiz_id, question_idx, attempt_idx)
    attempt.update(json.loads(attempt['questionJSON']))
    attempt.update(json.loads(attempt['answersJSON']))
    del attempt['questionJSON']
    del attempt['answersJSON']

    # this naming differs between attempt and result
    attempt['score'] = attempt['userScore']

    # add attempt_idx directly to final context
    context = {}
    context['attempt_idx'] = attempt_idx

    # render the appropriate page for this attempt
    return render_attempt_or_result(request, course_id, quiz_id, question_idx, attempt, context)


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
