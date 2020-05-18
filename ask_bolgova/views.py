from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, reverse

from django.contrib.auth.decorators import login_required

from ask_bolgova.paginator.paginate import paginate
from ask_bolgova.models import *

from urllib.parse import urlsplit

from ask_bolgova import forms


def index(request):
    question_list = Question.objects.new_questions()

    return render(request, 'index.html', paginate(question_list, request))


def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    comments = Comment.objects.filter(question_id=question_id)

    initial = {'question': question.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.profile

    if request.method == 'GET':
        form = forms.CommentForm(initial=initial)
    else:
        form = forms.CommentForm(initial=initial, data=request.POST)
        if form.is_valid():
            #comment = form.save()
            print(request.get_full_path())
            print(urlsplit(request.get_full_path()).query)
            #return render(request, 'question.html', {'question': question, 'comments': paginate(comments, request), 'form': form})
        else:
            print(form.author)

    return render(request, 'question.html', {'question': question, 'comments': paginate(comments, request), 'form': form})


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
            return redirect(question.get_absolute_url())

    return render(request, 'ask.html', {'form': form})


@login_required
def profile(request):
    user = get_object_or_404(User, username=request.user.username)
    if request.method == 'GET':
        form = forms.ProfileForm(initial={'nickname': user.profile.nickname}, instance=user)
    else:
        form = forms.ProfileForm(data=request.POST)
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                if key != 'avatar':
                    setattr(user, key, value)
                    setattr(user.profile, key, value)
                if request.FILES.get('avatar') is not None:
                    user.profile.avatar = request.FILES.get('avatar')
            user.save()
            return redirect('profile')
    return render(request, 'profile.html', {'form': form})


def view_profile(request, username):
    user = User.objects.get(username=username)
    if username == request.user.username:
        return redirect('profile')
    form = forms.ProfileForm(initial={'nickname': user.profile.nickname}, instance=user)
    return render(request, 'profile.html', {'form': form, 'user': user})


def login(request):
    next = request.POST.get('next', request.GET.get('next', ''))

    if request.method == 'GET':
        form = forms.LoginForm()
    else:
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            if form.user is not None:
                auth.login(request, form.user)
                if next and next != request.path:
                    return redirect(request.POST.get('next', reverse('index')))
                return redirect('index')
            else:
                return render(request, 'login.html', {'form': form, 'next': next})

    return render(request, 'login.html', {'form': form, 'next': next})


def logout(request):
    path_to_return = request.META.get('HTTP_REFERER', '/')
    auth.logout(request)
    return redirect(path_to_return)


def signup(request):
    if request.method == 'GET':
        form = forms.UserRegistrationForm()
    else:
        form = forms.UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.nickname = form.cleaned_data.get('nickname')
            user.profile.avatar = request.FILES.get('avatar', None)
            user.save()
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect('index')

    return render(request, 'signup.html', {'form': form})

