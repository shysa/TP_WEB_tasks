from django.http import Http404
from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from ask_bolgova.paginator.paginate import paginate
from ask_bolgova.models import *


def index(request):
    question_list = Question.objects.new_questions()

    return render(request, 'index.html', paginate(question_list, request))


def question(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        comments = Comment.objects.filter(question_id=question_id)
    except Question.DoesNotExist:
        raise Http404()

    return render(request, 'question.html', {'question': question, 'comments': comments})


def tag(request, tag):
    question_list = Question.objects.tag_questions(tag)

    return render(request, 'index.html', paginate(question_list, request))


def hot(request):
    question_list = Question.objects.best_questions()

    return render(request, 'index.html', paginate(question_list, request))


@login_required
def ask(request):
    return render(request, 'ask.html')


@login_required
def profile(request):
    return render(request, 'profile.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')
