from django import forms
from ask_bolgova.models import Question


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    #валидатор для юзернейма
    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError('Имя пользователя содержит пробелы')

        return username

    #проверить пароли на совпадение
    def clean(self):
        cdata = super().clean()
        pass


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