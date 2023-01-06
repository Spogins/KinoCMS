import json
import random
from datetime import datetime

from django.core.management.base import BaseCommand
from faker import Faker

from admin_app.models import Cinema, Gallery, Image, SeoBlock, Hall

fake = Faker('ru_RU')
lorem_ru = 'Важно заботиться о пациенте, чтобы за ним следовал клиент, но в то же время он будет страдать от больших болей и страданий. Ибо, говоря в мельчайших подробностях, никто не должен заниматься какой-либо работой, если он не извлечет из нее какой-либо пользы.Не злиться на боль, на выговор в наслаждении, он хочет быть волоском от боли, в надежде, что размножения нет. Если они не ослеплены похотью, они не выходят наружу; виноваты те, кто оставляет свои обязанности и смягчает свое сердце, то есть труд.'
lorem_uk = 'Важливо дбати про пацієнта, щоб за ним слідував клієнт, але в той же час він страждатиме від великих болю та страждань. Бо, говорячи в найдрібніших подробицях, ніхто не повинен займатися будь-якою роботою, якщо він не витягне з неї будь-якої користі. Не злитися на біль, на догану в насолоді, він хоче бути волоском від болю, сподіваючись, що розмноження немає. Якщо вони не засліплені пожадливістю, вони не виходять назовні; винні ті, хто залишає свої обов язки та пом якшує своє серце, тобто працю.'


def hall_scheme(scheme_name, hall_id):
    scheme = [random.randint(10, 20) for x in range(10)]
    new_data = {f'{hall_id}': scheme}
    with open(scheme_name, mode='r', encoding='utf8') as file:
        scheme_data = json.load(file)

        scheme_data['schemes'].update(new_data)
        with open(scheme_name, mode='w', encoding='utf8') as outfile:
            json.dump(scheme_data, outfile)


class Command(BaseCommand):
    def handle(self, *args, **options):
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