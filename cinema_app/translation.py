from modeltranslation.translator import register, TranslationOptions
from admin_app.models import *


@register(Film)
class FilmTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Cinema)
class CinemaTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'terms')


@register(Hall)
class HallTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(NewsPromotions)
class NewsPromotionsTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(HomePage)
class HomePageTranslationOptions(TranslationOptions):
    fields = ('seo_text',)


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Seance)
class PageTranslationOptions(TranslationOptions):
    fields = ('film_name',)

