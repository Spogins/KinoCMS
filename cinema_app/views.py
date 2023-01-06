import json
from datetime import datetime, timedelta
from random import choice
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from faker import Faker
from faker.generator import random
from admin_app.forms import *
from admin_app.models import *
from users.forms import CustomUserChangeForm
from users.models import CustomUser
fake = Faker('ru_RU')

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def home(request):
    carousel = get_object_or_404(CarouselBanner, type='carousel_home')
    carousel_news = get_object_or_404(CarouselBanner, type='carousel_promo')
    carousel_img = HomeBanner.objects.all()
    carousel_news_img = PromotionBanner.objects.all()
    now_date = now().date()
    db_movies = Film.objects.all()

    context = {
        'carousel_img': carousel_img,
        'carousel_news_img': carousel_news_img,
        'interval': carousel.interval,
        'interval_news': carousel_news.interval,
        'active': carousel.active,
        'active_news': carousel_news.active,
        'now_date': now_date,
        'movies': db_movies,
    }

    return render(request, 'cinema_app/home.html', context=context)


def films(request):
    db_movies = Film.objects.all()
    now_date = now().date()

    context = {
        'now_date': now_date,
        'movies': db_movies,
    }
    return render(request, 'cinema_app/films.html', context=context)


TIME = random.randint(100, 250)
FILM_INFO = {
    'year': random.randint(1990, 2020),
    'country': choice(['США', 'Англия', 'Германия', 'Франция', 'Италия']),
    'composer': f'{fake.first_name()} {fake.last_name()}',
    'producer': f'{fake.first_name()} {fake.last_name()}',
    'director': f'{fake.first_name()} {fake.last_name()}',
    'screenwriter': f'{fake.first_name()} {fake.last_name()}',
    'operator': f'{fake.first_name()} {fake.last_name()}',
    'genre': choice(['драма', 'комедия', 'трилер', 'ужасы', 'романтика', 'комедия, трилер', 'драма, романтика', 'трилер, фентези, ужасы',]),
    'budget': f'{random.randint(5, 15)} млн USD',
    'age': choice(['14', '18', '21']),
    'time': f'{TIME} мин. / {str(TIME/60)[0:4]}',
}


def film_card(request, film_id):
    show = get_object_or_404(Film, id=film_id)
    gallery = Image.objects.filter(gallery_id=show.gallery_id)
    _cinemas = Cinema.objects.all()
    context = {
        'show': show,
        'gallery': gallery,
        'cinemas': _cinemas,
        'film_info': FILM_INFO,
        'weak': [datetime.now().date() + timedelta(days=day) for day in range(7)],
    }
    return render(request, 'cinema_app/film_card.html', context=context)


def seances(request):
    if is_ajax(request):
        cinema_id = request.POST['cinema_id']
        film_id = request.POST['film_id']
        weak = [datetime.now().date() + timedelta(days=day) for day in range(7)]
        _seances = Seance.objects.filter(film_id=film_id, cinema_id=cinema_id, date__gte=now().date(), date__lte=weak[-1])
        context = []
        for elem in _seances:
            hall = Hall.objects.get(id=elem.hall_id)
            seance = {
                'seance': elem.id,
                'date': elem.date,
                'time': elem.time,
                'type': elem.type,
                'hall': hall.name,
                'price': elem.ticket_price,
            }
            context.append(seance)
        return JsonResponse({'context': context})
    return JsonResponse({'error': 'no_post'})


def show_scheme(scheme_name, hall_id):
    with open(scheme_name, mode='r', encoding='Latin-1') as scheme:
        scheme_data = json.load(scheme)
    return [int(place) for place in scheme_data['schemes'][f'{hall_id}']]


def booking(request, seance_id):
    seance = Seance.objects.get(id=seance_id)
    film = Film.objects.get(id=seance.film_id)
    hall = Hall.objects.get(id=seance.hall_id)
    context = {
        'seance': seance,
        'film': film,
        'hall': hall,
        'hall_scheme': show_scheme(hall.scheme_file, hall.id)
    }
    return render(request, 'cinema_app/booking.html', context=context)


def booking_place(request, seance_id):
    user_id = request.user.id
    if is_ajax(request) and request.method == 'POST':
        selected_place = json.loads(request.POST['selected_place'])
        _type = request.POST['type']
        if selected_place:
            for ticket in selected_place:
                _new_ticket = Ticket.objects.create(
                    place=ticket,
                    user=user_id,
                    seance=seance_id,
                    date=now().date()
                )
                if _type == 'booking':
                    _new_ticket.reserve = True
                else:
                    _new_ticket.sell = True
                _new_ticket.save()
            return JsonResponse({_type: selected_place})
    tickets = Ticket.objects.filter(user=user_id, seance=seance_id)
    no_available = Ticket.objects.filter(seance=seance_id).exclude(user=user_id)

    context = {
        'reserved': [],
        'sold': [],
        'no_available': []
    }
    for ticket in no_available:
        context['no_available'].append(ticket.place)
    for ticket in tickets:
        if ticket.reserve:
            context['reserved'].append(ticket.place)
        if ticket.sell:
            context['sold'].append(ticket.place)
    return JsonResponse(context)


def soon(request):
    db_movies = Film.objects.all()
    now_date = now().date()

    context = {
        'now_date': now_date,
        'movies': db_movies,
    }
    return render(request, 'cinema_app/soon.html', context=context)


def schedule(request):
    _cinemas = Cinema.objects.all()
    _films = Film.objects.all()
    halls = Hall.objects.all()
    _seances = Seance.objects.all()
    print(_seances[0].date)
    weak = [datetime.now().date() + timedelta(days=day) for day in range(7)]
    context = {
        'cinemas': _cinemas,
        'weak': weak,
        'f_day': weak[0],
        'l_day': weak[-1],
        'films': _films,
        'halls': halls,
        'seances': _seances,
    }
    if request.GET.get('film'):
        context['show_film'] = request.GET.get('film')
    if request.GET.get('cinema'):
        context['show_cinema'] = request.GET.get('cinema')
    if request.GET.get('hall'):
        context['show_hall'] = request.GET.get('hall')

    return render(request, 'cinema_app/schedule.html', context=context)


def schedule_seances(request):
    _seances = Seance.objects.all()
    if request.POST['cinema_id'] != 'all':
        _seances = _seances.filter(cinema_id=request.POST['cinema_id'])
    if request.POST['film_id'] != 'all':
        _seances = _seances.filter(film_id=request.POST['film_id'])
    if request.POST['hall_id'] != 'all':
        _seances = _seances.filter(hall_id=request.POST['hall_id'])

    seance_type = []
    if request.POST['type_2d'] == 'true':
        seance_type.extend(_seances.filter(type='2D'))

    if request.POST['type_3d'] == 'true':
        seance_type.extend(_seances.filter(type='3D'))

    if request.POST['type_imax'] == 'true':
        seance_type.extend(_seances.filter(type='IMAX'))

    if request.POST['type_imax'] == 'true' or request.POST['type_3d'] == 'true' or request.POST['type_2d'] == 'true':
        _seances = seance_type

    context = []
    for elem in _seances:
        seance = {
            'film_name': Film.objects.get(id=elem.film_id).name,
            'film_id': elem.film_id,
            'seance': elem.id,
            'date': elem.date,
            'time': elem.time,
            'type': elem.type,
            'hall_id': elem.hall_id,
            'hall_name': elem.hall_name,
            'price': elem.ticket_price,
        }
        context.append(seance)

    return JsonResponse({'context': context})


def cinemas(request):
    db_cinemas = Cinema.objects.all()

    context = {
        'cinemas': db_cinemas,
    }
    return render(request, 'cinema_app/cinemas.html', context=context)


def cinema_card(request, cinema_id):
    cinema_bd = Cinema.objects.get(id=cinema_id)
    hall = Hall.objects.filter(cinema_id=cinema_id)
    seance = Seance.objects.filter(cinema_id=cinema_id, date=now().date())
    gallery = Image.objects.filter(gallery_id=cinema_bd.gallery_id)
    context = {
        'cinema': cinema_bd,
        'halls': hall,
        'hall_ct': len(hall),
        'seances': seance,
        'gallery': gallery
    }
    return render(request, 'cinema_app/cinema_card.html', context=context)


def hall_card(request, cinema_id, hall_id):
    hall = Hall.objects.get(id=hall_id)
    hall_scheme = show_scheme(hall.scheme_file, hall.id)
    seance = Seance.objects.filter(cinema_id=cinema_id, hall_id=hall_id, date=now().date())
    gallery = Image.objects.filter(gallery_id=hall.gallery_id)
    context = {
        'hall': hall,
        'hall_scheme': hall_scheme,
        'seances': seance,
        'gallery': gallery,
        'cinema_id': cinema_id

    }
    return render(request, 'cinema_app/hall_card.html', context=context)


def promotions(request):
    events_obj = NewsPromotions.objects.filter(type='events', active=True)
    paginator = Paginator(events_obj, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'promotions': page_obj,
        'pages': paginator.page(1).has_other_pages()
    }
    return render(request, 'cinema_app/promotions.html', context=context)


def promo_card(request, promo_id):
    promo = NewsPromotions.objects.get(id=promo_id)
    gallery = Image.objects.filter(gallery_id=promo.gallery_id)
    context = {
        'promo': promo,
        'gallery': gallery
    }
    return render(request, 'cinema_app/promo_card.html', context=context)


def news(request):
    news_obj = NewsPromotions.objects.filter(type='news', active=True)
    paginator = Paginator(news_obj, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'news': page_obj,
        'pages': paginator.page(1).has_other_pages()
    }
    return render(request, 'cinema_app/news.html', context=context)


def news_card(request, news_id):
    _news = NewsPromotions.objects.get(id=news_id)
    gallery = Image.objects.filter(gallery_id=_news.gallery_id)
    context = {
        'news': _news,
        'gallery': gallery
    }
    return render(request, 'cinema_app/news_card.html', context=context)


def contacts(request):
    _contacts = CinemaContact.objects.all()
    context = {
        'contacts': _contacts,

    }
    return render(request, 'cinema_app/contacts.html', context=context)


def info(request, page):
    if page.isdigit():
        _page = Page.objects.get(id=page)
    else:
        _page = Page.objects.get(type=page)

    gallery = Image.objects.filter(gallery_id=_page.gallery_id)
    context = {
        'page': _page,
        'gallery': gallery
    }
    return render(request, 'cinema_app/info.html', context=context)


def show_user(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    form = CustomUserChangeForm(request.POST or None, instance=user)

    if request.method == 'POST':
        if form.is_valid():
            if form.cleaned_data['password'] != '' and form.cleaned_data['r_password'] != '':
                user.set_password(form.cleaned_data['password'])
            form.save()
            return redirect(f'/users/{user_id}')

    context = {
        'form': form,
    }
    return render(request, 'cinema_app/show_user.html', context=context)


# class Search(ListView):
#     def get_queryset(self):
#         _films = Film.objects.filter(name__icontains=self.request.GET.get('search'))
#         return render(self.request, 'cinema_app/search.html', {'films': 'asd'})
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['search'] = self.request.GET.get('search')
#         return render(self.request, 'cinema_app/search.html', {'films': 'asd'})
#

def search(request):
    context = {'fail': 'Film Name no match!'}
    if request.GET.get('search'):
        _films = Film.objects.filter(name__icontains=request.GET.get('search'))
        context = {
            'films': _films,
            'date': now().date()
        }
        print(_films)

    return render(request, 'cinema_app/search.html', context=context)