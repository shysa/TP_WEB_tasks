from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
import random

from ask_bolgova.models import *

from faker import Faker
fake = Faker()


class Command(BaseCommand):
    help = u'Заполнение базы данных случайными вопросами'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help=u'Количество создаваемых постов')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        author_list = User.objects.all()
        tag_list = Tag.objects.all()

        for i in range(total):
            a = random.choice(author_list)
            q = Question.objects.create(title=fake.sentence(), text=fake.text(),
                                        author=a.profile)

            for x in range(random.randint(1, 3)):
                t = random.choice(tag_list)
                q.tags.add(t)
            q.save()
