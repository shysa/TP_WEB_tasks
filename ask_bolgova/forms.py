from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from ask_bolgova.models import Question, Comment


class LoginForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError('Имя пользователя содержит пробелы')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Такого пользователя не существует')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if ' ' in password:
            raise forms.ValidationError('Пароль содержит пробелы')
        return password

    def clean(self):
        cdata = super().clean()
        username = cdata.get('username')
        password = cdata.get('password')

        if username and password:
            if not self.errors:
                user = authenticate(username=username, password=password)
                if user is None:
                    errors = {'password': ValidationError('Введен неверный пароль')}
                    raise ValidationError(errors)
                self.user = user

        return cdata


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label="Логин")
    email = forms.EmailField()
    nickname = forms.CharField(label="Никнейм")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повторите пароль")
    avatar = forms.ImageField(label="Загрузить аватар", required=False)

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if ' ' in nickname:
            raise forms.ValidationError('Никнейм содержит пробелы')
        return nickname

    def clean_password2(self):
        password2 = self.cleaned_data['password2']
        if not password2:
            raise forms.ValidationError('Введите пароль повторно')
        return password2

    def clean_avatar(self):
        url = self.cleaned_data['avatar']
        extensions = ['jpg', 'jpeg', 'png']
        url_ext = url.split('.', 1)[1].lower()
        if url_ext not in extensions:
            raise forms.ValidationError('Недопустимый формат изображения')
        return url

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if ' ' in password1:
            errors = {'password1': ValidationError('Пароль содержит пробелы')}
            raise forms.ValidationError(errors)

        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Введенные пароли не совпадают'),
                      'password1': ValidationError('')}
            raise ValidationError(errors)

    class Meta:
        model = User
        fields = ('username', 'email', 'nickname', 'password1', 'password2', 'avatar')


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def __init__(self, author, *args, **kwargs):
        self.author = author
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        question = Question(**self.cleaned_data)
        question.author = self.author
        if commit:
            question.save()
        return question


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'question', 'author']
        widgets = {
            #'question': forms.HiddenInput,
            #'author': forms.HiddenInput,
            'text': forms.Textarea(attrs={'placeholder': 'Введите ваш комментарий', 'rows': 4})
        }

    def save(self, commit=True):
        comment = Comment(**self.cleaned_data)
        if commit:
            comment.save()
        return comment


class ProfileForm(forms.ModelForm):
    email = forms.EmailField()
    nickname = forms.CharField(label="Никнейм")
    avatar = forms.ImageField(label="Аватар", required=False)

    # def __init__(self, request_user, *args, **kwargs):
    #   self.request_user = request_user
    #   super().__init__(*args, **kwargs)

    def clean_nickname(self):
        username = self.cleaned_data['nickname']
        if ' ' in username:
            raise forms.ValidationError('Никнейм содержит пробелы')
        return username

    def clean_avatar(self):
        url = self.cleaned_data['avatar']
        extensions = ['jpg', 'jpeg', 'png']
        url_ext = url.split('.', 1)[1].lower()
        if url_ext not in extensions:
            raise forms.ValidationError('Недопустимый формат изображения')
        return url

    class Meta:
        model = User
        fields = ['email', 'nickname', 'avatar']
