from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('films/', films, name='films'),
    path('films/<int:film_id>', film_card, name='film_card'),
    path('films/seances/', seances, name='seances'),
    path('soon/', soon, name='soon'),
    path('seances/', schedule_seances, name='schedule_seances'),
    path('schedule/', schedule, name='schedule'),
    path('schedule/booking/<int:seance_id>', booking, name='booking'),
    path('booking/<int:seance_id>/place', booking_place, name='booking_place'),
    path('cinemas/', cinemas, name='cinemas'),
    path('cinemas/<int:cinema_id>', cinema_card, name='cinema_card'),
    path('cinemas/<int:cinema_id>/<int:hall_id>', hall_card, name='hall_card'),
    path('promotions/', promotions, name='promotions'),
    path('promotions/<int:promo_id>', promo_card, name='promo_card'),
    path('news/', news, name='news_page'),
    path('news/<int:news_id>', news_card, name='news_card'),
    path('info/<page>', info, name='info'),
    path('contacts/', contacts, name='contacts_page'),
    path('users/<int:user_id>', show_user, name='show_user'),
    path('search/', search, name='search'),
]
