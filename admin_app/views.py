import json
from datetime import timedelta
from math import floor
from celery.result import AsyncResult
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required
from django.db.utils import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from admin_app.forms import *
from admin_app.models import *
from django.utils.timezone import now
from users.forms import *
from users.models import CustomUser
from .tasks import send_email_task


def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(f'/admin_page')
        else:
            return render(request, 'admin_app/login_admin.html', {'error': 'Не верный имя пользователя или пароль'})

    return render(request, 'admin_app/login_admin.html')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


# Create your views here.
def save_db(form, seo_form, gallery_formset, name=False):
    seo_form.save()
    full_form = form.save(commit=False)
    full_form.seo = seo_form.instance
    gallery = Gallery.objects.create(text=full_form.name)
    full_form.gallery = get_object_or_404(Gallery, id=gallery.id)
    for image in gallery_formset:
        if image.cleaned_data:
            images = image.save(commit=False)
            images.gallery = full_form.gallery
            images.save()
    gallery_formset.save()
    if name:
        full_form.type = name
    full_form.save()
    return full_form.id


def update_db(show, form, seo_form, gallery_formset):
    seo_form.save()
    form.seo = seo_form.instance
    form.save()
    gallery = show.gallery
    for image in gallery_formset:
        if image.cleaned_data:
            images = image.save()
            images.gallery = gallery
            images.save()
    for form in gallery_formset.deleted_forms:
        form.instance.delete()


@permission_required('request.user.is_superuser', login_url=login_admin)
def index(request):
    _users = CustomUser.objects.filter(is_staff=False, is_superuser=False)
    tickets = Ticket.objects.all()
    weak = [(now().date() - timedelta(days=day)) for day in range(7)]
    context = {
        'user_gender': [len(_users.filter(gender='male')), len(_users.filter(gender='female'))],
        'user_reg': len(_users),
        'ticket_range': [len(tickets.filter(date=day)) for day in weak][::-1],
        'weak': weak,
        'booking': [len(tickets.filter(reserve=True)), len(tickets.filter(sell=True))]
    }
    return render(request, 'admin_app/index.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def movies(request):
    now_date = now().date()
    db_movies = Film.objects.all()
    context = {
        'now_date': now_date,
        'movies': db_movies,
        'title': 'ADMIN'
    }
    return render(request, 'admin_app/films.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def films_page(request):
    form = FilmCardForm(request.POST or None, request.FILES or None, prefix='film_form')
    seo_form = SeoForm(request.POST or None, prefix='seo_form')
    gallery_formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.none(),
                                   prefix='gallery_formset')

    if request.method == 'POST':
        if gallery_formset.is_valid() and seo_form.is_valid() and form.is_valid():
            save_db(form, seo_form, gallery_formset)
            return redirect(f'/admin_page/movie/')

    context = {
        'name': 'Название фильма',
        'descript': 'Описание',
        'form': form,
        'seo_form': seo_form,
        'gallery_formset': gallery_formset}

    return render(request, 'admin_app/film_page.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def show_film(request, film_id):
    show = get_object_or_404(Film, id=film_id)
    form = FilmCardForm(request.POST or None, request.FILES or None, prefix='form', instance=show)
    seo_form = SeoForm(request.POST or None, prefix='seo_form', instance=show.seo)
    gallery_formset = ImageFormSet(
        request.POST or None,
        request.FILES or None,
        queryset=Image.objects.filter(gallery=show.gallery.id),
        prefix='gallery_formset',
    )
    if request.method == 'POST':
        if gallery_formset.is_valid() and seo_form.is_valid() and form.is_valid():
            update_db(show, form, seo_form, gallery_formset)
            return redirect(f'/admin_page/movie/')

    context = {
        'name': 'Название фильма',
        'descript': 'Описание',
        'show': show,
        'form': form,
        'gallery_formset': gallery_formset,
        'seo_form': seo_form,
    }
    return render(request, 'admin_app/film.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def delete_film(request, film_id):
    film_for_del = Film.objects.get(pk=film_id)
    film_for_del.seo.delete()
    film_for_del.gallery.delete()
    seances = Seance.objects.filter(film_id=film_id)
    for seance in seances:
        seance.delete()
    film_for_del.delete()
    return redirect(f'/admin_page/movie/')


@permission_required('request.user.is_superuser', login_url=login_admin)
def banner(request):
    home_banner_formset = HomeBannerFormSet(request.POST or None, request.FILES or None,
                                            queryset=HomeBanner.objects.all(),
                                            prefix='home_banner_formset')
    promo_banner_formset = PromoBannerFormSet(request.POST or None, request.FILES or None,
                                              queryset=PromotionBanner.objects.all(), prefix='promo_banner_formset')

    bg_banner = get_object_or_404(BackgroundBanner)
    bg_banner_form = BackBannerForm(request.POST or None, request.FILES or None, instance=bg_banner)

    carousel_home = get_object_or_404(CarouselBanner, type='carousel_home')
    carousel_home_form = CarouselBannerForm(request.POST or None, prefix='carousel_home', instance=carousel_home)

    carousel_promo = get_object_or_404(CarouselBanner, type='carousel_promo')
    carousel_promo_form = CarouselBannerForm(request.POST or None, prefix='carousel_promo', instance=carousel_promo)

    if request.method == 'POST':

        if home_banner_formset.is_valid() and promo_banner_formset.is_valid() and bg_banner_form.is_valid():
            carousel_home_form.save()
            carousel_promo_form.save()

            bg_banner_form.save()

            if not bg_banner.bg_image:
                bg_banner.type = False
                bg_banner.save()

            for b_form in home_banner_formset:
                if b_form.cleaned_data:
                    banner = b_form.save(commit=False)
                    banner.save()

            for form in home_banner_formset.deleted_forms:
                form.instance.delete()

            for p_form in promo_banner_formset:
                if p_form.cleaned_data:
                    p_banner = p_form.save(commit=False)
                    p_banner.save()

            for form_p in promo_banner_formset.deleted_forms:
                form_p.instance.delete()

            return redirect('/admin_page/banner')

    context = {
        'home_banner_formset': home_banner_formset,
        'promo_banner_formset': promo_banner_formset,
        'bg_banner_form': bg_banner_form,
        'carousel_home_form': carousel_home_form,
        'carousel_promo_form': carousel_promo_form
    }
    return render(request, 'admin_app/banner.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def news(request):
    news_obj = NewsPromotions.objects.filter(type='news')
    context = {
        'news': news_obj,
    }
    return render(request, 'admin_app/news.html', context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def news_page(request):
    form = NewsPromoCardForm(request.POST or None, request.FILES or None, prefix='news_form')
    seo_form = SeoForm(request.POST or None, prefix='seo_form')
    gallery_formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.none(),
                                   prefix='gallery_formset')
    if request.method == 'POST':
        if gallery_formset.is_valid() and seo_form.is_valid() and form.is_valid():
            save_db(form, seo_form, gallery_formset, 'news')
            return redirect('/admin_page/news/')

    context = {
        'name': 'Название новости',
        'descript': 'Описание',
        'form': form,
        'seo_form': seo_form,
        'gallery_formset': gallery_formset}
    return render(request, 'admin_app/news_events_page.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def show_news(request, news_id):
    show = get_object_or_404(NewsPromotions, id=news_id)
    form = NewsPromoCardForm(request.POST or None, request.FILES or None, prefix='news_form', instance=show)
    seo_form = SeoForm(request.POST or None, prefix='seo_form', instance=show.seo)
    gallery_formset = ImageFormSet(
        request.POST or None,
        request.FILES or None,
        queryset=Image.objects.filter(gallery=show.gallery.id),
        prefix='gallery_formset',
    )

    if request.method == 'POST':
        if gallery_formset.is_valid() and seo_form.is_valid() and form.is_valid():
            update_db(show, form, seo_form, gallery_formset)
            return redirect(f'/admin_page/news/')

    context = {
        'name': 'Название новости',
        'descript': 'Описание',
        'show': show,
        'form': form,
        'gallery_formset': gallery_formset,
        'seo_form': seo_form,
    }
    return render(request, 'admin_app/show_news_events.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def events(request):
    events_obj = NewsPromotions.objects.filter(type='events')
    context = {
        'events': events_obj,
    }
    return render(request, 'admin_app/events.html', context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def events_page(request):
    form = NewsPromoCardForm(request.POST or None, request.FILES or None, prefix='events_form')
    seo_form = SeoForm(request.POST or None, prefix='seo_form')
    gallery_formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.none(),
                                   prefix='gallery_formset')
    if request.method == 'POST':
        if gallery_formset.is_valid() and seo_form.is_valid() and form.is_valid():
            save_db(form, seo_form, gallery_formset, 'events')
            return redirect('/admin_page/events/')

    context = {
        'name': 'Название акции',
        'descript': 'Описание',
        'form': form,
        'seo_form': seo_form,
        'gallery_formset': gallery_formset}
    return render(request, 'admin_app/news_events_page.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def show_events(request, event_id):
    show = get_object_or_404(NewsPromotions, id=event_id)
    form = NewsPromoCardForm(request.POST or None, request.FILES or None, prefix='events_form', instance=show)
    seo_form = SeoForm(request.POST or None, prefix='seo_form', instance=show.seo)
    gallery_formset = ImageFormSet(
        request.POST or None,
        request.FILES or None,
        queryset=Image.objects.filter(gallery=show.gallery.id),
        prefix='gallery_formset',
    )

    if request.method == 'POST':
        if gallery_formset.is_valid() and seo_form.is_valid() and form.is_valid():
            update_db(show, form, seo_form, gallery_formset)
            return redirect(f'/admin_page/events/')

    context = {
        'name': 'Название акции',
        'descript': 'Описание',
        'show': show,
        'form': form,
        'gallery_formset': gallery_formset,
        'seo_form': seo_form,
    }
    return render(request, 'admin_app/show_news_events.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def delete_news(request, news_id):
    news_for_del = NewsPromotions.objects.get(pk=news_id)
    news_for_del.seo.delete()
    news_for_del.gallery.delete()
    news_for_del.delete()
    return redirect(f'/admin_page/news/')


@permission_required('request.user.is_superuser', login_url=login_admin)
def delete_events(request, event_id):
    event_for_del = NewsPromotions.objects.get(pk=event_id)
    event_for_del.seo.delete()
    event_for_del.gallery.delete()
    event_for_del.delete()
    return redirect(f'/admin_page/events/')


@permission_required('request.user.is_superuser', login_url=login_admin)
def cinemas(request):
    cinemas_obj = Cinema.objects.all()

    context = {
        'cinemas_obj': cinemas_obj,
    }
    return render(request, 'admin_app/cinemas.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def cinemas_page(request):
    form = CinemaForm(request.POST or None, request.FILES or None, prefix='form')
    seo_form = SeoForm(request.POST or None, prefix='seo_form')
    gallery_formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.none(),
                                   prefix='gallery_formset')

    if request.method == 'POST':
        if gallery_formset.is_valid() and seo_form.is_valid() and form.is_valid():
            cinema_id = save_db(form, seo_form, gallery_formset)
            return redirect(f'/admin_page/cinemas/{cinema_id}')

    context = {
        'cinema_hall': 'Логотип',
        'name': 'Название кинотеатра',
        'descript': 'Описание',
        'terms': 'Условия',
        'form': form,
        'seo_form': seo_form,
        'gallery_formset': gallery_formset}
    return render(request, 'admin_app/cinemas_page.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def show_cinema(request, cinema_id):
    show = get_object_or_404(Cinema, id=cinema_id)
    form = CinemaForm(request.POST or None, request.FILES or None, prefix='form', instance=show)
    seo_form = SeoForm(request.POST or None, prefix='seo_form', instance=show.seo)
    gallery_formset = ImageFormSet(
        request.POST or None,
        request.FILES or None,
        queryset=Image.objects.filter(gallery=show.gallery.id),
        prefix='gallery_formset',
    )

    halls = Hall.objects.filter(cinema=cinema_id)

    if request.method == 'POST':
        if gallery_formset.is_valid() and seo_form.is_valid() and form.is_valid():
            update_db(show, form, seo_form, gallery_formset)
            return redirect(f'/admin_page/cinemas/')

    context = {
        'cinema_hall': 'Логотип',
        'name': 'Название кинотеатра',
        'descript': 'Описание',
        'terms': 'Условия',
        'show': show,
        'form': form,
        'gallery_formset': gallery_formset,
        'seo_form': seo_form,
        'halls': halls
    }
    return render(request, 'admin_app/show_cinema.html', context=context)


HALL_SCHEME = "hall_scheme.json"


def hall_scheme(scheme_name, hall_id, scheme):
    new_data = {f'{hall_id}': scheme}
    with open(scheme_name, mode='r', encoding='utf8') as file:
        scheme_data = json.load(file)

        scheme_data['schemes'].update(new_data)
        with open(scheme_name, mode='w', encoding='utf8') as outfile:
            json.dump(scheme_data, outfile)


@permission_required('request.user.is_superuser', login_url=login_admin)
def hall_page(request, cinema_id):
    form = HallForm(request.POST or None, request.FILES or None, prefix='form')
    seo_form = SeoForm(request.POST or None, prefix='seo_form')
    gallery_formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.none(),
                                   prefix='gallery_formset')
    report = ''
    if request.method == 'POST':

        if gallery_formset.is_valid() and seo_form.is_valid() and form.is_valid():
            try:
                full_form = form.save(commit=False)
                seo_form.save()
                full_form.seo = seo_form.instance
                gallery = Gallery.objects.create(text=full_form.name)
                full_form.gallery = get_object_or_404(Gallery, id=gallery.id)
                for image in gallery_formset:
                    if image.cleaned_data:
                        images = image.save(commit=False)
                        images.gallery = full_form.gallery
                        images.save()
                gallery_formset.save()
                full_form.date = now().date()
                full_form.cinema = get_object_or_404(Cinema, id=cinema_id)
                full_form.save()
                hall_scheme(HALL_SCHEME, full_form.id, request.POST.getlist('place_row'))
                full_form.scheme_file = HALL_SCHEME
                full_form.save()
                return redirect(f'/admin_page/cinemas/{cinema_id}')
            except IntegrityError:
                report = 'Зал с таким именем уже существует!'

    context = {
        'report': report,
        'cinema_hall': 'Верхний баннер',
        'name': 'Номер зала',
        'descript': 'Описание',
        'form': form,
        'seo_form': seo_form,
        'gallery_formset': gallery_formset}
    return render(request, 'admin_app/hall_page.html', context=context)


def show_scheme(scheme_name, hall_id):
    with open(scheme_name, mode='r', encoding='Latin-1') as scheme:
        scheme_data = json.load(scheme)
    return [int(place) for place in scheme_data['schemes'][f'{hall_id}']]


@permission_required('request.user.is_superuser', login_url=login_admin)
def show_hall(request, cinema_id, hall_id):
    show = get_object_or_404(Hall, id=hall_id)
    form = HallForm(request.POST or None, request.FILES or None, prefix='form', instance=show)
    seo_form = SeoForm(request.POST or None, prefix='seo_form', instance=show.seo)
    gallery_formset = ImageFormSet(
        request.POST or None,
        request.FILES or None,
        queryset=Image.objects.filter(gallery=show.gallery.id),
        prefix='gallery_formset',
    )

    if request.method == 'POST':
        if gallery_formset.is_valid() and seo_form.is_valid() and form.is_valid():
            update_db(show, form, seo_form, gallery_formset)
            hall_scheme(HALL_SCHEME, show.id, request.POST.getlist('place_row'))
            return redirect(f'/admin_page/cinemas/{cinema_id}')

    context = {
        'show': show,
        'hall_scheme': show_scheme(HALL_SCHEME, show.id),
        'cinema_hall': 'Верхний баннер',
        'name': 'Номер зала',
        'descript': 'Описание',
        'form': form,
        'seo_form': seo_form,
        'gallery_formset': gallery_formset}
    return render(request, 'admin_app/show_hall.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def delete_hall(request, cinema_id, hall_id):
    event_for_del = Hall.objects.get(pk=hall_id)
    event_for_del.seo.delete()
    event_for_del.gallery.delete()
    seances = Seance.objects.filter(film_id=hall_id)
    for seance in seances:
        seance.delete()
    event_for_del.delete()
    return redirect(f'/admin_page/cinemas/{cinema_id}')


@permission_required('request.user.is_superuser', login_url=login_admin)
def delete_cinema(request, cinema_id):
    cinema = Cinema.objects.get(pk=cinema_id)
    hall_obj = Hall.objects.filter(pk=cinema_id)
    for hall in hall_obj:
        hall.seo.delete()
        hall.gallery.delete()
        hall.delete()
    seances = Seance.objects.filter(film_id=cinema_id)
    for seance in seances:
        seance.delete()
    cinema.seo.delete()
    cinema.gallery.delete()
    cinema.delete()
    return redirect(f'/admin_page/cinemas/')


@permission_required('request.user.is_superuser', login_url=login_admin)
def pages(request):
    base = Page.objects.filter(can_delete=False)
    pages_obj = Page.objects.filter(can_delete=True)
    home_obj = get_object_or_404(HomePage)
    contacts_obj = get_object_or_404(Contact)
    context = {
        'contacts': contacts_obj,
        'base': base,
        'pages': pages_obj,
        'home': home_obj
    }
    return render(request, 'admin_app/pages.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def create_page(request):
    form = PageForm(request.POST or None, request.FILES or None, prefix='form')
    seo_form = SeoForm(request.POST or None, prefix='seo_form')
    gallery_formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.none(),
                                   prefix='gallery_formset')

    if request.method == 'POST':
        if gallery_formset.is_valid() and seo_form.is_valid() and form.is_valid():
            save_db(form, seo_form, gallery_formset)
            return redirect(f'/admin_page/pages/')

    context = {
        'name': 'Название',
        'descript': 'Описание',
        'form': form,
        'seo_form': seo_form,
        'gallery_formset': gallery_formset
    }
    return render(request, 'admin_app/create_page.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def show_page(request, page_id):
    show = get_object_or_404(Page, id=page_id)
    form = PageForm(request.POST or None, request.FILES or None, prefix='form', instance=show)
    seo_form = SeoForm(request.POST or None, prefix='seo_form', instance=show.seo)
    gallery_formset = ImageFormSet(
        request.POST or None,
        request.FILES or None,
        queryset=Image.objects.filter(gallery=show.gallery.id),
        prefix='gallery_formset',
    )

    if request.method == 'POST':
        if gallery_formset.is_valid() and seo_form.is_valid() and form.is_valid():
            update_db(show, form, seo_form, gallery_formset)
            return redirect(f'/admin_page/pages/')

    context = {
        'show': show,
        'name': 'Название',
        'descript': 'Описание',
        'form': form,
        'seo_form': seo_form,
        'gallery_formset': gallery_formset
    }
    return render(request, 'admin_app/show_page.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def delete_page(request, page_id):
    page_for_del = Page.objects.get(pk=page_id)
    page_for_del.seo.delete()
    page_for_del.gallery.delete()
    page_for_del.delete()
    return redirect(f'/admin_page/pages/')


@permission_required('request.user.is_superuser', login_url=login_admin)
def home_page(request):
    home_obj = get_object_or_404(HomePage)
    form = HomePageForm(request.POST or None, request.FILES or None, instance=home_obj)
    seo_form = SeoForm(request.POST or None, prefix='seo_form', instance=home_obj.seo)
    if request.method == 'POST':
        if seo_form.is_valid() and form.is_valid():
            seo_form.save()
            form.seo = seo_form.instance
            form.save()
            return redirect(f'/admin_page/pages/')

    context = {
        'form': form,
        'seo_form': seo_form
    }

    return render(request, 'admin_app/home_page.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def contacts(request):
    contacts_obj = get_object_or_404(Contact)
    form = ContactsForm(request.POST or None, instance=contacts_obj)
    seo_form = SeoForm(request.POST or None, prefix='seo_form', instance=contacts_obj.seo)
    cinema_contact_formset = CinemaContactFormSet(request.POST or None, request.FILES or None,
                                                  queryset=CinemaContact.objects.all(),
                                                  prefix='cinema_contact_formset')

    if request.method == 'POST':
        if seo_form.is_valid() and form.is_valid() and cinema_contact_formset.is_valid():
            seo_form.save()
            form.seo = seo_form.instance
            form.save()
            for form in cinema_contact_formset:
                if form.cleaned_data:
                    cinema_form = form.save()
                    cinema_form.save()
            for cinema_contact in cinema_contact_formset.deleted_forms:
                cinema_contact.instance.delete()
            return redirect(f'/admin_page/pages/')

    context = {
        'form': form,
        'seo_form': seo_form,
        'cinema_contact_formset': cinema_contact_formset
    }

    return render(request, 'admin_app/contacts.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def mailing(request):
    form_mail_template = MailingTemplateForm(request.POST or None, request.FILES or None,)
    form_users = UserMailingForm(request.POST or None)
    user_list = CustomUser.objects.filter(is_staff=False, is_superuser=False)
    last_templates = MailingTemplate.objects.order_by('-pk')[:5]

    if is_ajax(request):
        mail_list = False
        mails = json.loads(request.POST.get('user_emails'))

        if not request.POST['concrete_temp'] == '':
            if request.POST['all_users'] == 'on':
                all_users_emails = user_list.values_list('email', flat=True)
                mail_list = [mail for mail in all_users_emails]
            elif len(mails) > 0:
                mail_list = mails

            if mail_list:
                if request.POST['concrete_temp'] == request.POST['load_temp']:
                    file = request.FILES
                    template = MailingTemplate.objects.create(html_template=file.get('html_template'))
                    template.save()
                    html_template = template.html_template.name
                else:
                    html_template = request.POST['concrete_temp']

                html_message = render_to_string(html_template)
                task = send_email_task.delay(mail_list, html_message)
                return JsonResponse({'task_id': task.task_id}, status=202)

    context = {
        'form_users': form_users,
        'form_mail_template': form_mail_template,
        'users': user_list,
        'user_ct': len(user_list),
        'last_templates': last_templates
    }
    return render(request, 'admin_app/mailing.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def mailing_progress(request, task_id):
    task = AsyncResult(task_id)
    if task.state == 'FAILURE':
        response = {
            'task_id': task_id,
            'state': task.state,
            'progress': '0',
        }
        return JsonResponse(response, status=200)
    elif task.state == 'SUCCESS':
        response = {
            'task_id': task_id,
            'state': task.state,
            'progress': '100%',
        }
        return JsonResponse(response, status=200)
    done = task.info.get('done') + 1
    total = task.info.get('total')
    progress = floor((100 / int(total)) * int(done))

    response = {
        'task_id': task_id,
        'state': task.state,
        'progress': progress,
    }
    return JsonResponse(response, status=200)


@permission_required('request.user.is_superuser', login_url=login_admin)
def template_delete(request, template_id):
    template = MailingTemplate.objects.get(pk=template_id)
    template.delete()
    response = {
        'template_id': template_id
    }
    return JsonResponse(response)


@permission_required('request.user.is_superuser', login_url=login_admin)
def users(request):
    users_obj = CustomUser.objects.filter(is_staff=False, is_superuser=False)
    context = {
        'users': users_obj,
    }
    return render(request, 'admin_app/users.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def show_user(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    form = CustomUserChangeForm(request.POST or None, instance=user)

    if request.method == 'POST':
        if form.is_valid():
            if form.cleaned_data['password'] != '' and form.cleaned_data['r_password'] != '':
                user.set_password(form.cleaned_data['password'])
            form.save()
            return redirect(f'/admin_page/users/')

    context = {
        'form': form,
    }
    return render(request, 'admin_app/show_user.html', context=context)


@permission_required('request.user.is_superuser', login_url=login_admin)
def delete_user(request, user_id):
    user_for_del = CustomUser.objects.get(pk=user_id)
    user_for_del.delete()
    return redirect(f'/admin_page/users/')


