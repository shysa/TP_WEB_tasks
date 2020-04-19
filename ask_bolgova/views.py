from django.contrib import auth
from django.shortcuts import render, get_object_or_404, redirect, reverse

from django.contrib.auth.decorators import login_required

from ask_bolgova.paginator.paginate import paginate
from ask_bolgova.models import *

from ask_bolgova import forms

def index(request):
    question_list = Question.objects.new_questions()

    return render(request, 'index.html', paginate(question_list, request))


def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    comments = Comment.objects.filter(question_id=question_id)

    return render(request, 'question.html', {'question': question, 'comments': paginate(comments, request)})


def tag(request, tag):
    question_list = Question.objects.tag_questions(tag)

    return render(request, 'index.html', paginate(question_list, request))


def hot(request):
    question_list = Question.objects.best_questions()

    return render(request, 'index.html', paginate(question_list, request))


@login_required
def ask(request):
    if request.method == 'GET':
        form = forms.QuestionForm(request.user.profile)
    else:
        form = forms.QuestionForm(request.user.profile, data=request.POST)
        if form.is_valid():
            question = form.save()
            return redirect(reverse('question', kwargs={'question_id': question.pk}))

    return render(request, 'ask.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'profile.html')


def login(request):
    if request.method == 'GET':
        form = forms.LoginForm()
    else:
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect('/')    # TODO: правильный редирект! должен происходить туда, откуда пользователь был направлен на страницу логина

    return render(request, 'login.html', {'form': form})


def signup(request):
    return render(request, 'signup.html')
