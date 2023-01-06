from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

User = get_user_model()
fake = Faker('ru_RU')


class Command(BaseCommand):
    def handle(self, *args, **options):
        admin_user = User.objects.create(
            is_superuser=True,
            is_staff=True,
            is_active=True,
            username='admin'
        )
        admin_user.set_password('qwerty52Rt')
        admin_user.save()
        sub_admin = User.objects.create(
            is_superuser=True,
            is_staff=True,
            is_active=True,
            username='admin2',
        )
        sub_admin.set_password('qwertyBaba31')
        sub_admin.save()
        print("ADMIN CREATED!")
