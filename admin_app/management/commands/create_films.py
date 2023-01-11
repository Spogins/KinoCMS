from datetime import date, datetime
from random import choice


from faker import Faker
from django.core.management.base import BaseCommand
from admin_app.models import Film, SeoBlock, Gallery, Image

fake = Faker('ru_RU')

lorem_ru = 'Важно заботиться о пациенте, чтобы за ним следовал клиент, но в то же время он будет страдать от больших болей и страданий. Ибо, говоря в мельчайших подробностях, никто не должен заниматься какой-либо работой, если он не извлечет из нее какой-либо пользы.Не злиться на боль, на выговор в наслаждении, он хочет быть волоском от боли, в надежде, что размножения нет. Если они не ослеплены похотью, они не выходят наружу; виноваты те, кто оставляет свои обязанности и смягчает свое сердце, то есть труд.'
lorem_uk = 'Важливо дбати про пацієнта, щоб за ним слідував клієнт, але в той же час він страждатиме від великих болю та страждань. Бо, говорячи в найдрібніших подробицях, ніхто не повинен займатися будь-якою роботою, якщо він не витягне з неї будь-якої користі. Не злитися на біль, на догану в насолоді, він хоче бути волоском від болю, сподіваючись, що розмноження немає. Якщо вони не засліплені пожадливістю, вони не виходять назовні; винні ті, хто залишає свої обов язки та пом якшує своє серце, тобто працю.'
trailer = 'https://www.youtube.com/embed/Mnb_3ibUp38'
FILMS_NAMES = [
    {'name_ru': 'План 9 из космоса', 'name_uk': 'План 9 з космосу'},
    {'name_ru': 'Геймеры', 'name_uk': 'Геймери'},
    {'name_ru': 'Фрайтмар', 'name_uk': 'Фрайтмер'},
    {'name_ru': 'Рептилия', 'name_uk': 'Рептилія'},
    {'name_ru': 'Начало конца', 'name_uk': 'Початок кінця'},
    {'name_ru': 'Штурм муравья', 'name_uk': 'Штурм мурахи'},
    {'name_ru': 'Невидимый человек', 'name_uk': 'Невидима людина'},
    {'name_ru': 'Черный кот', 'name_uk': 'Чорний кіт'},
    {'name_ru': 'Атака помидоров-убийц', 'name_uk': 'Атака помідорів-вбивць'},
]


def create_seo():
    seo_block = SeoBlock.objects.create(
        url='https://www.youtube.com/',
        title='Title',
        keywords='Keywords',
        description=lorem_ru,
    )
    seo_block.save()
    return seo_block.id


class Command(BaseCommand):
    def handle(self, *args, **options):
        for num in range(10):
            film = Film.objects.create(
                name_ru='Название Фильма №'+str(1 + num),
                name_uk='Назва Фільму №'+str(1 + num),
                image='#',
                premier_date=fake.date_between(start_date=datetime(2019, 1, 10), end_date=datetime(2024, 5, 10)),
                description_ru=lorem_ru,
                description_uk=lorem_uk,
                v2d=choice([True, False]),
                v3d=choice([True, False]),
                imax=choice([True, False]),
                trailer=trailer
            )
            if not film.v2d and not film.v3d and not film.imax:
                film.v2d = True
            gallery = Gallery.objects.create(text=film.name)
            gallery.save()

            film.seo = SeoBlock.objects.get(id=create_seo())
            film.gallery = gallery
            film.save()
            print("Film created")