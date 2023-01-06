from django import forms
from django.utils.timezone import now
from .models import *
from django.forms import modelformset_factory


class FilmCardForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = {'description_ru', 'description_uk', 'image', 'trailer', 'v3d', 'v2d', 'imax', 'premier_date', 'name_uk', 'name_ru'}
        widgets = {
            'name_ru': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Название Фильма...'}),
            'name_uk': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Назва...'}),
            'description_ru': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Описание...'}),
            'description_uk': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Опис...'}),
            'image': forms.FileInput(attrs={
                'id': 'inputfile',
                'type': 'file',
                'name': 'files[]',
                'class': 'imageInput',
                'accept': '.jpg, .img, .png, .gif',
                'style': 'display: none'}),
            'trailer': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Ссылкана видео...'}),
            'v3d': forms.CheckboxInput(attrs={
                'class': 'checkbox'}),
            'v2d': forms.CheckboxInput(attrs={
                'class': 'checkbox'}),
            'imax': forms.CheckboxInput(attrs={
                'class': 'checkbox'}),
            'premier_date': forms.DateInput(attrs={
                'type': 'date',
                'value': now().date()
            }, format='%Y-%m-%d')
        }


class SeoForm(forms.ModelForm):
    class Meta:
        model = SeoBlock
        fields = {'url', 'title', 'keywords', 'description'}
        widgets = {
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'URL'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Title'}),
            'keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Keywords'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Description'}),
        }


class ImageForm(forms.ModelForm):
    class Meta:
        madel = Image
        fields = ('image',)
        widgets = {
            'image': forms.FileInput(attrs={
                'type': 'file',
                'name': 'files[]',
                'class': 'imageInput',
                'accept': '.jpg, .img, .png, .gif',
                'style': 'display: none'}),
        }


class BackBannerForm(forms.ModelForm):
    class Meta:
        model = BackgroundBanner
        fields = ('bg_image', 'color', 'type')
        widgets = {
            'bg_image': forms.FileInput(attrs={
                'id': 'inputfile',
                'type': 'file',
                'name': 'files[]',
                'class': 'imageInput',
                'accept': '.jpg, .img, .png, .gif',
                'style': 'display: none',
            }),
            'color': forms.TextInput(attrs={
                'type': 'color',
                'name': 'bg_color',
                'id': 'bg_color'}),
            'type': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'type': 'radio',
                'onclick': 'bgType(bg_photo)',
                'id': 'bg_photo',
            })
        }


class HomeBannerForm(forms.ModelForm):
    class Meta:
        model = HomeBanner
        fields = ('image', 'url', 'text')
        widgets = {
            'image': forms.FileInput(attrs={
                'type': 'file',
                'name': 'files[]',
                'class': 'imageInput',
                'accept': '.jpg, .img, .png, .gif',
                'style': 'display: none'}),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'URL'}),
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Text'}),
        }


class PromoBannerForm(forms.ModelForm):
    class Meta:
        model = PromotionBanner
        fields = ('image', 'url')
        widgets = {
            'image': forms.FileInput(attrs={
                'type': 'file',
                'name': 'files[]',
                'class': 'imageInput',
                'accept': '.jpg, .img, .png, .gif',
                'style': 'display: none'}),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'URL'}),
        }


class CarouselBannerForm(forms.ModelForm):
    class Meta:
        model = CarouselBanner
        rotate_choice = (('3000', '3c'), ('5000', '5c'), ('7000', '7c'), ('10000', '10c'))
        fields = ('active', 'interval')
        widgets = {
            'active': forms.CheckboxInput(attrs={
                'type': 'checkbox',
                'class': 'form-check-input',
                'role': 'switch',
            }),
            'interval': forms.Select(
                attrs={
                    'class': 'form-select'
                },
                choices=rotate_choice
            )
        }


class NewsPromoCardForm(forms.ModelForm):
    class Meta:
        model = NewsPromotions
        fields = {'name_uk', 'name_ru', 'description_ru', 'description_uk', 'image', 'video', 'post_date', 'active'}
        widgets = {
            'name_ru': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Название...'}),
            'name_uk': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Назва...'}),
            'description_ru': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Описание...'}),
            'description_uk': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Опис...'}),
            'image': forms.FileInput(attrs={
                'id': 'inputfile',
                'type': 'file',
                'name': 'files[]',
                'class': 'imageInput',
                'accept': '.jpg, .img, .png, .gif',
                'style': 'display: none'}),
            'video': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Ссылкана видео...'}),
            'post_date': forms.DateInput(attrs={
                'type': 'date',
            }),
            'active': forms.CheckboxInput(attrs={
                'type': 'checkbox',
                'class': 'form-check-input',
                'role': 'switch',
            }),
        }


class CinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = {'name_ru', 'description_ru', 'terms_ru', 'name_uk', 'description_uk', 'terms_uk', 'image', 'banner_image'}
        widgets = {
            'name_ru': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Название кинотеатра...'}),
            'description_ru': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Описание...'}),
            'terms_ru': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Условия...'}),
            'name_uk': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Назва...'}),
            'description_uk': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Опис...'}),
            'terms_uk': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Условия...'}),
            'image': forms.FileInput(attrs={
                'id': 'inputfile',
                'type': 'file',
                'name': 'files[]',
                'class': 'imageInput',
                'accept': '.jpg, .img, .png, .gif',
                'style': 'display: none'}),
            'banner_image': forms.FileInput(attrs={
                'id': 'inputbanner',
                'type': 'file',
                'name': 'files[]',
                'class': 'imageInput',
                'accept': '.jpg, .img, .png, .gif',
                'style': 'display: none'}),
        }


class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = {'name', 'description_ru', 'description_uk', 'image'}
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'integer',
                'placeholder': 'Номер зала...'}),
            'description_ru': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Описание...'}),
            'description_uk': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Опис...'}),
            'image': forms.FileInput(attrs={
                'id': 'inputfile',
                'type': 'file',
                'name': 'files[]',
                'class': 'imageInput',
                'accept': '.jpg, .img, .png, .gif',
                'style': 'display: none'}),
        }


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = {'name_uk', 'name_ru', 'description_ru', 'description_uk', 'active', 'image', 'date'}
        widgets = {
            'name_ru': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Название...'}),
            'name_uk': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Назва...'}),
            'description_ru': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Описание...'}),
            'description_uk': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Опис...'}),
            'image': forms.FileInput(attrs={
                'id': 'inputfile',
                'type': 'file',
                'name': 'files[]',
                'class': 'imageInput',
                'accept': '.jpg, .img, .png, .gif',
                'style': 'display: none'}),
            'active': forms.CheckboxInput(attrs={
                'type': 'checkbox',
                'class': 'form-check-input',
                'role': 'switch'}),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'value': now().date()}, format='%Y-%m-%d')
        }


class HomePageForm(forms.ModelForm):
    class Meta:
        model = HomePage
        fields = {'active', 'phone_0', 'phone_1', 'seo_text_ru', 'seo_text_uk', 'date'}
        widgets = {
            'phone_0': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'integer',
                'placeholder': '000-000-00-00'}),
            'phone_1': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'integer',
                'placeholder': '000-000-00-00'}),
            'seo_text_ru': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'SEO текст...'}),
            'seo_text_uk': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'SEO текст...'}),
            'active': forms.CheckboxInput(attrs={
                'type': 'checkbox',
                'class': 'form-check-input',
                'role': 'switch'}),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'value': now().date()
            }, format='%Y-%m-%d')
        }


class ContactsForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = {'date', 'active'}
        widgets = {
            'active': forms.CheckboxInput(attrs={
                'type': 'checkbox',
                'class': 'form-check-input',
                'role': 'switch'}),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'value': now().date()
            }, format='%Y-%m-%d')
        }


class CinemaContactForm(forms.ModelForm):
    class Meta:
        model = CinemaContact
        fields = {'name', 'address', 'location', 'logo'}
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Название кинотеатра...'}),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': f'Кинотеатр...\nАдресс...\nБронирование билетов...\ne-mail...'}),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Координаты для карты...'}),
            'logo': forms.FileInput(attrs={
                'id': 'inputfile',
                'type': 'file',
                'name': 'files[]',
                'class': 'imageInput',
                'accept': '.jpg, .img, .png, .gif',
                'style': 'display: none'}),
        }


class MailingTemplateForm(forms.ModelForm):
    class Meta:
        model = MailingTemplate
        fields = {'html_template'}
        widgets = {
            'html_template': forms.FileInput(attrs={
                'id': 'html_template',
                'type': 'file',
                'name': 'file_input',
                'accept': '.html',
                'style': 'display: none',
            })
        }


class UserMailingForm(forms.Form):
    all_users = forms.BooleanField(initial=True, label='', required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'type': 'radio',
        'id': 'all_users',
        'onclick': 'switchMailing(this)'
    }))
    ch_users = forms.BooleanField(initial=False, label='', required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'type': 'radio',
        'id': 'ch_users',
        'onclick': 'switchMailing(this)'
    }))


class PasswordForm(forms.Form):
    password = forms.CharField(max_length=30, required=False, widget=forms.PasswordInput(attrs={
        'id': 'password',
        'class': 'form-control',
        'placeholder': 'Пароль...'
    }))
    confirm_password = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'id': 'confirm_password',
        'class': 'form-control',
        'placeholder': 'Подтвердить пароль...',
        'type': 'password'
    }))


ImageFormSet = modelformset_factory(model=Image, form=ImageForm, extra=0, can_delete=True, labels=None)
ImageFormSet.deletion_widget = forms.CheckboxInput(attrs={'class': 'delete_form', 'style': 'display: none'})

HomeBannerFormSet = modelformset_factory(model=HomeBanner, form=HomeBannerForm, extra=0, can_delete=True,
                                         labels=None)
HomeBannerFormSet.deletion_widget = forms.CheckboxInput(attrs={'class': 'delete_form'})

PromoBannerFormSet = modelformset_factory(model=PromotionBanner, form=PromoBannerForm, extra=0, can_delete=True,
                                          labels=None)
PromoBannerFormSet.deletion_widget = forms.CheckboxInput(attrs={'class': 'delete_form'})

CinemaContactFormSet = modelformset_factory(model=CinemaContact, form=CinemaContactForm, extra=0, can_delete=True,
                                            labels=None)
CinemaContactFormSet.deletion_widget = forms.CheckboxInput(attrs={'class': 'delete_form'})
