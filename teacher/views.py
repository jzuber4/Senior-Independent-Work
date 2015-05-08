import json
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_http_methods
from quiz_service import service as qs
from quiz_service.models import Course, Quiz
from quiz_service.service import NotFound

# Create your views here.
@login_required
@user_passes_test(lambda u: u.userinfo.is_teacher)
def index(request):
    courses = qs.get_admin_courses(request.user.username)
    courses = sorted(courses.items(), key=lambda c: int(c[0]))
    d = {
        'teacher_site': True,
        'courses': courses,
    }
    # update db info for courses
    for id, title in courses:
        course, created = Course.objects.get_or_create(service_id=id)
        if created or title != course.title:
            course.title = title
            course.save()
    return render(request, "teacher/index.html", d)

@login_required
@user_passes_test(lambda u: u.userinfo.is_teacher)
def create(request, course_id):
    course_id = int(course_id)
    if request.method == 'GET':
        question_types_and_titles = qs.get_question_types()
        question_types, question_titles = zip(*sorted(question_types_and_titles.items()))
        grading_types_and_titles = qs.get_grading_types().items()
        d = {
            'course_id' : course_id,
            'page_title' : 'Create a Quiz',
            'teacher_site': True,
            'title': "",
            'timeLimitEnabled': False,
            'timeLimit': 240,
            'perQuestionTimeLimitEnabled': True,
            'perQuestionTimeLimit': 30,
            'perQuestionNumAttempts': 5,
            'perQuestionMaxScore': 5,
            'gradingType': grading_types_and_titles[0][0],
            'question_titles': json.dumps(question_titles),
            'question_types': json.dumps(question_types),
            'grading_types_and_titles': grading_types_and_titles,
            'questions': [],
        }
        return render(request, 'teacher/create.html', d)
    else:
        # yyyy-MM-dd HH:mm:ss
        post = request.POST
        minutes = post.get('timeLimit') if post.get('timeLimitEnabled') == "on" else 0
        formatFrom = "%Y/%m/%d %H:%M"
        formatTo = "%Y-%m-%d %H:%M:%S"
        startDate   = datetime.strptime(post.get('startDate'),   formatFrom).strftime(formatTo)
        softEndDate = datetime.strptime(post.get('softEndDate'), formatFrom).strftime(formatTo)
        endDate     = datetime.strptime(post.get('endDate'),     formatFrom).strftime(formatTo)
        quiz = {
            'courseId':     course_id,
            'title':        post.get('title'),
            'numQuestions': int(post.get('numQuestions')),
            'startDate':    startDate,
            'softEndDate':  softEndDate,
            'endDate':      endDate,
            'minutes':      int(minutes),
        }
        questions = []
        questionTypes             = post.getlist('questionType')
        questionTitles            = post.getlist('questionTitle')
        questionMaxScores         = post.getlist('questionMaxScore')
        questionNumAttempts       = post.getlist('questionNumAttempts')
        questionGradingTypes      = post.getlist('questionGradingType')
        questionTimeLimits        = post.getlist('questionTimeLimit')
        questionTimeLimitsEnabled = post.getlist('questionTimeLimitEnabled')
        for i in range(int(post.get('numQuestions'))):
            questions.append({
                'questionIdx': (i+1),
                'questionType': questionTypes[i],
                'title':        questionTitles[i],
                'maxScore':     int(float(questionMaxScores[i])),
                'maxAttempts':  int(questionNumAttempts[i]),
                'grading':      questionGradingTypes[i],
                'minutes': int(questionTimeLimits[i]) if questionTimeLimitsEnabled[i] == "on" else 0,
            })
        if post.get('is_edit'):
            for q in questions:
                q['quizId'] = post.get('quiz_id')
            quiz['quizId'] = post.get('quiz_id')
            print("CALLING EDIT!")
            qs.edit_quiz(json.dumps(quiz), json.dumps(questions))
        else:
            print("CALLING MAKE!")
            qs.make_quiz(json.dumps(quiz), json.dumps(questions))
        print(quiz)
        print(questions)
        return redirect('teacher.views.course', course_id)


@login_required
@user_passes_test(lambda u: u.userinfo.is_teacher)
def course(request, course_id):
    course_id = int(course_id)

    # parse quizzes
    quizzes = []
    # quizzes come in id, json pairs
    try:
        course_quizzes = qs.get_course_quizzes(request.user.username, course_id)
    except NotFound:
        messages.error(request, 'Course {} not found'.format(course_id))
        return redirect('teacher.views.index')
    for quiz_id, rest in sorted(course_quizzes.items(), key=lambda q: int(q[0])):
        # decode the json into a dictionary
        quiz = json.loads(rest)
        # add the id back into the quiz
        quiz['quizId'] = quiz_id
        # parse the array of questions as json
        quiz['questions'] = [json.loads(q) for q in json.loads(quiz['questions'])]
        # precalculate the max score, it is not part of the quiz
        quiz['maxScore'] = sum(q['maxScore'] for q in quiz['questions'])
        quiz['startDate'] = parse_datetime(quiz['startDate'])
        quiz['softEndDate'] = parse_datetime(quiz['softEndDate'])
        quiz['endDate'] = parse_datetime(quiz['endDate'])
        quiz['timeLeft'] = timedelta(milliseconds=quiz['quizMaxMilliseconds'])
        quiz['is_timed'] = int(quiz['quizMaxMilliseconds']) > 0
        quizzes.append(quiz)
        # save the title in the db
        quiz_model, created = Quiz.objects.get_or_create(service_id=quiz_id)
        if created or quiz["title"] != quiz_model.title:
            quiz_model.title = quiz["title"]
            quiz_model.save()

    d = {
        'teacher_site': True,
        'course_id': course_id,
        # get the course title for display
        'course_title': Course.objects.get(service_id=course_id).title,
        'quizzes': quizzes,
    }

    return render(request, 'teacher/course.html', d)

@login_required
@user_passes_test(lambda u: u.userinfo.is_teacher)
def edit(request, course_id, quiz_id):
    course_id = int(course_id)
    quiz_id   = int(quiz_id)

    question_types_and_titles = qs.get_question_types()
    question_types, question_titles = zip(*sorted(question_types_and_titles.items()))
    grading_types_and_titles = qs.get_grading_types().items()

    formatTo   = "%Y/%m/%d %H:%M"
    formatFrom = "%Y-%m-%d %H:%M:%S"

    try:
        info = qs.get_admin_quiz_info(quiz_id)
    except NotFound:
        messages.error(request, 'Quiz {} not found'.format(quiz_id))
        return redirect('teacher.views.course', course_id)

    quiz = json.loads(info['quizJSON'])
    questions = [json.loads(q) for q in json.loads(info['questionsJSON'])]
    print(quiz)
    print(questions)

    # save title in db
    quiz_model, created = Quiz.objects.get_or_create(service_id=quiz_id)
    if created or quiz['title'] != quiz_model.title:
        quiz_model.title = quiz['title']
        quiz_model.save()

    for q in questions:
        q['type']        = q['questionType']
        q['timeLimit']   = q['minutes']
        q['checked']     = "checked='checked'" if int(q['minutes']) > 0 else ""
        q['numAttempts'] = q['maxAttempts']
        q['gradingType'] = q['grading']
    d = {
        'course_id': course_id,
        'course_title': Course.objects.get(service_id=course_id).title,
        'endDate':     datetime.strptime(quiz['endDate'], formatFrom).strftime(formatTo),
        'gradingType': questions[0]['grading'],
        'grading_types_and_titles': grading_types_and_titles,
        'is_edit': True,
        'page_title' : 'Editing Quiz {}'.format(quiz['quizId']),
        'perQuestionMaxScore': int(float(questions[0]['maxScore'])),
        'perQuestionNumAttempts': int(questions[0]['maxAttempts']),
        'perQuestionTimeLimit': int(questions[0]['minutes']),
        'perQuestionTimeLimitEnabled': int(questions[0]['minutes']) != 0,
        'questions': json.dumps(questions),
        'question_titles': json.dumps(question_titles),
        'question_types': json.dumps(question_types),
        'quiz_id': quiz_id,
        'quiz_title': quiz['title'],
        'startDate':   datetime.strptime(quiz['startDate'], formatFrom).strftime(formatTo),
        'softEndDate': datetime.strptime(quiz['softEndDate'], formatFrom).strftime(formatTo),
        'teacher_site': True,
        'timeLimit': int(quiz['minutes']),
        'timeLimitEnabled': int(quiz['minutes']) != 0,
        'title': quiz['title'],
    }

    return render(request, "teacher/create.html", d)



@login_required
@user_passes_test(lambda u: u.userinfo.is_teacher)
@require_http_methods(["POST"])
def delete(request, course_id, quiz_id):
    qs.delete_quiz(quiz_id)
    return redirect('teacher.views.course', course_id)
