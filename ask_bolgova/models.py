from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, BaseUserManager

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models import Sum, Count


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True)
    nickname = models.CharField(max_length=30)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username


# ----------------------------------------------------------------------------------------
class Tag(models.Model):
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.title


# ----------------------------------------------------------------------------------------
class LikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # Записи с рейтингом > 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # И < 0
        return self.get_queryset().filter(vote__lt=0)

    def rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def create(self, target, user, pk, vote_type):
        obj = target.__class__.objects.get(pk=pk)
        try:
            like = Like.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=user)
            if like.vote is not vote_type:
                like.vote = vote_type
                like.save(update_fields=['vote'])
            else:
                like.delete()
        except Like.DoesNotExist:
            obj.rating.create(user=user, vote=vote_type)


class Like(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.SmallIntegerField(choices=VOTES, default=0)

    user = models.ForeignKey(settings.AUTH_PROFILE_MODULE, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = LikeManager()

    def __str__(self):
        title = str(self.user) + " votes " + str(self.object_id) + " | " + str(self.content_type)
        return title


# ----------------------------------------------------------------------------------------
class QuestionManager(models.Manager):
    def best_questions(self):
        return self.get_queryset().order_by('-rating__vote').annotate(comment_count=Count('comment'))

    def new_questions(self):
        return self.get_queryset().order_by('-creating_date')[:10].annotate(comment_count=Count('comment'))

    def tag_questions(self, tag):
        return self.get_queryset().filter(tags__title__contains=tag).annotate(comment_count=Count('comment'))


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()

    creating_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    author = models.ForeignKey(settings.AUTH_PROFILE_MODULE, on_delete=models.CASCADE)
    rating = GenericRelation(Like, related_query_name='questions')

    tags = models.ManyToManyField(Tag, blank=True)

    objects = QuestionManager()

    class Meta:
        ordering = ['-creating_date']

    def get_absolute_url(self):
        return '/question/%d/' % self.pk

    def save_question(self):
        super(Question, self).save()

    def __str__(self):
        return self.title


# ----------------------------------------------------------------------------------------
class Comment(models.Model):
    text = models.TextField()
    best_comment = models.BooleanField(default=False)
    creating_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_PROFILE_MODULE, on_delete=models.CASCADE)

    rating = GenericRelation(Like, related_query_name='comments')

    def save_comment(self):
        super(Comment, self).save()

    def __str__(self):
        return self.text
