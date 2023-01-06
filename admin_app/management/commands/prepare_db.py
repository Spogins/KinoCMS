import json
import random
from datetime import timedelta
from random import choice

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.datetime_safe import datetime
from django.utils.timezone import now
from faker import Faker

from admin_app.models import *

User = get_user_model()
fake = Faker('ru_RU')
lorem_ru = 'Важно заботиться о пациенте, чтобы за ним следовал клиент, но в то же время он будет страдать от больших болей и страданий. Ибо, говоря в мельчайших подробностях, никто не должен заниматься какой-либо работой, если он не извлечет из нее какой-либо пользы.Не злиться на боль, на выговор в наслаждении, он хочет быть волоском от боли, в надежде, что размножения нет. Если они не ослеплены похотью, они не выходят наружу; виноваты те, кто оставляет свои обязанности и смягчает свое сердце, то есть труд.'
lorem_uk = 'Важливо дбати про пацієнта, щоб за ним слідував клієнт, але в той же час він страждатиме від великих болю та страждань. Бо, говорячи в найдрібніших подробицях, ніхто не повинен займатися будь-якою роботою, якщо він не витягне з неї будь-якої користі. Не злитися на біль, на догану в насолоді, він хоче бути волоском від болю, сподіваючись, що розмноження немає. Якщо вони не засліплені пожадливістю, вони не виходять назовні; винні ті, хто залишає свої обов язки та пом якшує своє серце, тобто працю.'
trailer = 'https://www.youtube.com/embed/Mnb_3ibUp38'
cinema_map = '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2742.721930412542!2d30.783534315594864!3d46.572963979129646!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x40c6252b9939e271%3A0x12a33aabb602d8bd!2z0JrQuNC90L7RgtC10LDRgtGAICLQl9Cy0LXQt9C00L3Ri9C5Ig!5e0!3m2!1sru!2sua!4v1672489952348!5m2!1sru!2sua" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'


def create_carousel(name):
    print(f'Создание CarouselBanner.{name}...')
    carousel = CarouselBanner.objects.create(
        type=name,
        active=False,
        interval=5000
    )
    carousel.save()
    print(f'CarouselBanner.{name} Создан.')


page_type = {
    'cinema': 'О кинотеатре',
    'cafe': 'Кафе - Бар',
    'vip': 'Vip-зал',
    'adv': 'Реклама',
    'child': 'Детская комната',
}


def create_page(name):
    print(f'Создание Page.{name}...')
    page = Page.objects.create(
        type=name,
        can_delete=False,
        active=False,
        name=page_type[name],
        description_ru=lorem_ru,
        description_uk=lorem_uk,
        date=now().date(),
        image='#'
    )
    seo_block = SeoBlock.objects.create()
    seo_block.save()
    gallery = Gallery.objects.create()
    gallery.save()
    page.seo = SeoBlock.objects.get(id=seo_block.id)
    page.gallery = Gallery.objects.get(id=gallery.id)
    page.save()
    print(f'Page.{name} Создан.')


def hall_scheme(scheme_name, hall_id):
    scheme = [random.randint(10, 20) for x in range(10)]
    new_data = {f'{hall_id}': scheme}
    with open(scheme_name, mode='r', encoding='utf8') as file:
        scheme_data = json.load(file)

        scheme_data['schemes'].update(new_data)
        with open(scheme_name, mode='w', encoding='utf8') as outfile:
            json.dump(scheme_data, outfile)


def create_admin():
    if not User.objects.filter(is_staff=True, is_superuser=True).exists():
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


def create_users():
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
            print(f'{x + 1}й пользователь добавлен...')
        print('Пользователи добавлены.')


def create_films():
    if not Film.objects.all():
        for num in range(10):
            film = Film.objects.create(
                name_ru='Название Фильма №' + str(1 + num),
                name_uk='Назва Фільму №' + str(1 + num),
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
            seo_block = SeoBlock.objects.create()
            seo_block.save()
            gallery = Gallery.objects.create(text=film.name)
            gallery.save()

            film.seo = seo_block
            film.gallery = gallery
            film.save()
            print("Film created")


def create_news_events():
    _page_type = {
        'news': {
            'name_ru':'Название Новости №',
            'name_uk': 'Назва Новини №',
        },
        'events': {
            'name_ru': 'Название Акции №',
            'name_uk': 'Назва Акції №',
        }
    }
    if not NewsPromotions.objects.all():
        for _type in ['news', 'events']:
            for num in range(4):
                obj = NewsPromotions.objects.create(
                    name_ru=f"{_page_type[_type]['name_ru']} {num}",
                    name_uk=f"{_page_type[_type]['name_uk']} {num}",
                    description_ru=lorem_ru,
                    description_uk=lorem_uk,
                    image='#',
                    post_date=now().date(),
                    type=_type,
                    video='https://www.youtube.com/',
                    active=True,
                )
                seo_block = SeoBlock.objects.create()
                seo_block.save()
                gallery = Gallery.objects.create(text=obj.name)
                gallery.save()
                obj.seo = seo_block
                obj.gallery = gallery
                obj.save()
                print(f"{_page_type[_type]['name_ru']} {num} created")


def create_cinema_and_halls():
    if not Cinema.objects.all():
        with open("hall_scheme.json", mode='w', encoding='utf8') as outfile:
            json.dump({'schemes': {}}, outfile)
        print('file hall_scheme.json created')

        for num in range(3):
            cinema = Cinema.objects.create(
                name_ru='Название Кинотеатра №' + str(1 + num),
                name_uk='Назва Кінотеатру №' + str(1 + num),
                image='#',
                banner_image='#',
                date=fake.date_between(start_date=datetime(2019, 1, 10), end_date=datetime(2024, 5, 10)),
                description_ru=lorem_ru,
                description_uk=lorem_uk,
                terms_ru=lorem_ru,
                terms_uk=lorem_uk,
            )
            seo_block = SeoBlock.objects.create()
            seo_block.save()
            gallery = Gallery.objects.create(text=cinema.name)
            gallery.save()
            cinema.seo = seo_block
            cinema.gallery = gallery
            cinema.save()
            for hall_num in range(3):
                hall = Hall.objects.create(
                    name=(1 + hall_num),
                    image='#',
                    date=fake.date_between(start_date=datetime(2019, 1, 10), end_date=datetime(2024, 5, 10)),
                    description_ru=lorem_ru,
                    description_uk=lorem_uk,
                    scheme_file="hall_scheme.json"
                )
                hall_scheme(hall.scheme_file, hall.id)
                hall.cinema = cinema
                seo_block = SeoBlock.objects.create()
                seo_block.save()
                gallery = Gallery.objects.create(text=hall.name)
                gallery.save()
                hall.seo = seo_block
                hall.gallery = gallery
                hall.save()
                print("Hall created")
            print("Cinema created")


def create_seances():
    if not Seance.objects.all():
        date_range = [datetime.now().date() + timedelta(days=day) for day in range(30)]
        time_range = [(datetime.combine(date=datetime.now(), time=datetime.now().time()) + timedelta(hours=x)).time()
                      for x in range(15)]
        list_halls = [hall.id for hall in Hall.objects.all()]
        list_films = []
        for film in Film.objects.all():
            if film.premier_date <= datetime.now().date():
                list_films.append(film.id)

        for day in date_range:
            for _time in time_range:
                seance_time = str(_time)
                seance = Seance.objects.get_or_create(
                    date=day,
                    time=seance_time[:-10],
                    ticket_price=choice([50, 70, 100, 120, 150]),
                    hall_id=choice(list_halls),
                    film_id=choice(list_films)
                )
                hall = Hall.objects.filter(id=seance[0].hall_id)
                seance[0].cinema_id = hall[0].cinema_id
                seance[0].hall_name = hall[0].name
                film = Film.objects.get(id=seance[0].film_id)
                seance[0].film_name_ru = film.name_ru
                seance[0].film_name_uk = film.name_uk
                film_types = []
                if film.v3d:
                    film_types.append('3D')
                if film.v2d:
                    film_types.append('2D')
                if film.imax:
                    film_types.append('IMAX')
                seance[0].type = choice(film_types)

                seance[0].save()
        print('Generate seances SUCCESS')


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Проверка на наличие обьектов...')

        create_admin()
        create_users()

        if not BackgroundBanner.objects.all():
            print('Создание BackgroundBanner...')
            bg_banner = BackgroundBanner.objects.create(
                type=False,
                color='#ccebff'
            )
            bg_banner.save()
            print('BackgroundBanner Создан...')

        if not CarouselBanner.objects.filter(type='carousel_home'):
            create_carousel('carousel_home')

        if not CarouselBanner.objects.filter(type='carousel_promo'):
            create_carousel('carousel_promo')

        if not HomePage.objects.all():
            print('Создание HomePage...')
            home_page = HomePage.objects.create(
                phone_0=25252525,
                phone_1=25252525,
                active=False,
                seo_text_ru=lorem_ru,
                seo_text_uk=lorem_uk
            )
            seo_block = SeoBlock.objects.create()
            seo_block.save()
            home_page.seo = SeoBlock.objects.get(id=seo_block.id)
            home_page.save()
            print('HomePage Создан.')

        if not Contact.objects.all():
            print('Создание Contact...')
            contact_page = Contact.objects.create()
            seo_block = SeoBlock.objects.create()
            seo_block.save()
            contact_page.seo = SeoBlock.objects.get(id=seo_block.id)
            contact_page.save()
            cinema_contact = CinemaContact.objects.create(
                name='Кинотеатр "Звездный"',
                address='Кинотеатр "Звездный", Одесса, Одесская область, 65000',
                location='https://www.google.de/maps/place/%D1%83%D0%BB.+%D0%9A%D0%B0%D0%BF%D0%B8%D1%82%D0%B0%D0%BD%D0%B0+%D0%9A%D1%83%D0%B7%D0%BD%D0%B5%D1%86%D0%BE%D0%B2%D0%B0,+98,+%D0%9E%D0%B4%D0%B5%D1%81%D1%81%D0%B0,+%D0%9E%D0%B4%D0%B5%D1%81%D1%81%D0%BA%D0%B0%D1%8F+%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C,+65000/@46.5728797,30.7857427,19.5z/data=!4m5!3m4!1s0x40c6252b8529da33:0x7bf965dfc54a048c!8m2!3d46.572714!4d30.7851793?hl=ru',
                logo='#'
            )
            cinema_contact.save()
            print('Contact Создан.')

        if not Page.objects.filter(type='cinema'):
            create_page('cinema')

        if not Page.objects.filter(type='cafe'):
            create_page('cafe')

        if not Page.objects.filter(type='vip'):
            create_page('vip')

        if not Page.objects.filter(type='adv'):
            create_page('adv')

        if not Page.objects.filter(type='child'):
            create_page('child')

        create_films()
        create_news_events()
        create_cinema_and_halls()
        create_seances()

        print('Обьекты созданы.')

