from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()
    nickname = models.CharField(max_length=30)


class Tag(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Like(models.Model):
    rating = models.IntegerField()


class QuestionManager(models.Manager):
    def best_questions(self):
        return self.order_by('-rating')

    def new_questions(self):
        return self.order_by('-creating_date')[:10]


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()

    creating_date = models.DateTimeField(blank=True)

    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rating = models.OneToOneField(Like, on_delete=models.DO_NOTHING)

    tags = models.ManyToManyField(Tag)

    objects = QuestionManager()

    class Meta:
        ordering = ['-creating_date']

    def __str__(self):
        return self.title


class Answer(models.Model):
    text = models.TextField()

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    rating = models.OneToOneField(Like, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.text
