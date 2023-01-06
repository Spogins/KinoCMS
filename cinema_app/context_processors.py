from django.shortcuts import get_object_or_404

from admin_app.models import *
from users.forms import CustomUserCreationForm


def registration(request):
    form = CustomUserCreationForm(request.POST or None)
    return {'register_form': form}


def base_page(request):
    home_obj = get_object_or_404(HomePage)
    contact1 = home_obj.phone_0
    contact2 = home_obj.phone_1
    context = {'contact1': contact1, 'contact2': contact2}
    if request.LANGUAGE_CODE == 'ru':
        context.update({'seo_text': home_obj.seo_text_ru})
    else:
        context.update({'seo_text': home_obj.seo_text_uk})

    return context


def background(request):
    bg_banner = get_object_or_404(BackgroundBanner)
    if bg_banner.type:
        return {'background': bg_banner.bg_image}
    else:
        return {'background': bg_banner.color}


def pages(request):
    _pages = Page.objects.filter(can_delete=True)
    return {'pages': _pages}