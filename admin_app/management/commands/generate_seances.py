from datetime import timedelta
from random import choice

from django.core.management.base import BaseCommand

from django.utils.datetime_safe import datetime, time

from admin_app.models import Hall, Film, Seance, Cinema


class Command(BaseCommand):

    date_range = [datetime.now().date() + timedelta(days=day) for day in range(7)]
    time_range = [(datetime.combine(date=datetime.now(), time=datetime.now().time()) + timedelta(hours=x)).time() for x in range(15)]
    list_halls = [hall.id for hall in Hall.objects.all()]
    list_films = []
    for film in Film.objects.all():
        if film.premier_date <= datetime.now().date():
            list_films.append(film.id)

    def handle(self, *args, **options):
        for day in self.date_range:
            for _time in self.time_range:
                seance_time = str(_time)
                seance = Seance.objects.get_or_create(
                    date=day,
                    time=seance_time[:-10],
                    ticket_price=choice([50, 70, 100, 120, 150]),
                    hall_id=choice(self.list_halls),
                    film_id=choice(self.list_films)
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
        self.stdout.write('Generate seances SUCCESS')