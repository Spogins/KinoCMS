from random import choice

from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth import get_user_model

User = get_user_model()
fake = Faker('ru_RU')


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(is_staff=False, is_superuser=False).exists():
            print('Создание пользователей...')
            for x in range(15):
                user = User.objects.create(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.email(),
                    username=fake.user_name(),
                    address=fake.address(),
                    card_number=fake.credit_card_number(),
                    birth_date=fake.date_of_birth(),
                    phone_number=fake.phone_number(),
                    city=fake.city(),
                    gender=choice(['male', 'female'])
                )
                user.set_password('Qwerty123456')
                user.save()
                print(f'{x+1}й пользователь добавлен...')
            print('Пользователи добавлены.')


