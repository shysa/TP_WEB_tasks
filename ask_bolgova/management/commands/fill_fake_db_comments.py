from django.core.management.base import BaseCommand

import random
from faker import Faker
fake = Faker()

from ask_bolgova.models import *


class Command(BaseCommand):
    help = u'Заполнение базы данных случайными комментами'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help=u'Количество создаваемых комментов')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        author_list = User.objects.all()
        questions_list = Question.objects.all()

        for i in range(total):
            a = random.choice(author_list)
            q = random.choice(questions_list)
            com = Comment.objects.create(text=fake.text(), question=q, author=a.profile)
