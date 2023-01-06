from django.db import models
from django.urls import reverse


class Gallery(models.Model):
    text = models.CharField(max_length=100)


class Image(models.Model):
    image = models.ImageField(upload_to='images/gallery_images/', null=True, verbose_name='')
    gallery = models.ForeignKey('Gallery', on_delete=models.CASCADE, null=True)


class SeoBlock(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=300)
    keywords = models.CharField(max_length=300)
    description = models.TextField()


class Film(models.Model):
    date = models.DateField(null=True)
    name = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='images/films/', null=True, verbose_name='')
    premier_date = models.DateField()
    active = models.BooleanField(default=False)
    trailer = models.URLField(max_length=100)
    v3d = models.BooleanField(default=False)
    v2d = models.BooleanField(default=True)
    imax = models.BooleanField(default=False)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, null=True)
    seo = models.ForeignKey(SeoBlock, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('film', kwargs={'film_id': self.pk})


class Cinema(models.Model):
    date = models.DateField(null=True)
    name = models.CharField(max_length=300)
    description = models.TextField()
    terms = models.TextField()
    image = models.ImageField(upload_to='images/cinema/', null=True, verbose_name='')
    banner_image = models.ImageField(upload_to='images/cinema/', null=True, verbose_name='')
    gallery = models.ForeignKey('Gallery', on_delete=models.CASCADE, null=True)
    seo = models.ForeignKey('SeoBlock', on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('cinema', kwargs={'cinema_id': self.pk})


class Hall(models.Model):
    name = models.CharField(max_length=2)
    description = models.TextField()
    image = models.ImageField(upload_to='images/hall/', null=True, verbose_name='')
    date = models.DateField(null=True)
    cinema = models.ForeignKey('Cinema', on_delete=models.CASCADE, null=True)
    gallery = models.ForeignKey('Gallery', on_delete=models.CASCADE, null=True)
    seo = models.ForeignKey('SeoBlock', on_delete=models.CASCADE, null=True)
    scheme_file = models.CharField(null=True, max_length=100)

    class Meta:
        unique_together = [['name', 'cinema']]


class BackgroundBanner(models.Model):
    bg_image = models.ImageField(upload_to='images/bg_banner/', null=True, verbose_name='', blank=True)
    color = models.CharField(max_length=300, blank=True)
    type = models.BooleanField(default=False)


class HomeBanner(models.Model):
    image = models.ImageField(upload_to='images/home_banner/', null=True, verbose_name='')
    url = models.URLField(max_length=100)
    text = models.CharField(max_length=300)


class PromotionBanner(models.Model):
    image = models.ImageField(upload_to='images/promo_banner/', null=True, verbose_name='')
    url = models.URLField(max_length=100)


class CarouselBanner(models.Model):
    type = models.CharField(max_length=300)
    active = models.BooleanField(default=False)
    interval = models.IntegerField(null=True)


class NewsPromotions(models.Model):
    date = models.DateField(null=True)
    type = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='images/news_events/', null=True, verbose_name='')
    post_date = models.DateField()
    video = models.URLField(max_length=100)
    active = models.BooleanField(default=False)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, null=True)
    seo = models.ForeignKey(SeoBlock, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('show_news', kwargs={'news_id': self.pk})

    def get_event_url(self):
        return reverse('show_events', kwargs={'event_id': self.pk})


class HomePage(models.Model):
    active = models.BooleanField(default=False)
    date = models.DateField(null=True)
    phone_0 = models.IntegerField()
    phone_1 = models.IntegerField()
    seo_text = models.TextField()
    seo = models.ForeignKey(SeoBlock, on_delete=models.CASCADE, null=True)


class Page(models.Model):
    type = models.CharField(max_length=300, null=True)
    date = models.DateField(null=True)
    can_delete = models.BooleanField(default=True)
    name = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='images/pages/', null=True, verbose_name='')
    active = models.BooleanField(default=False)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, null=True)
    seo = models.ForeignKey(SeoBlock, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('show_page', kwargs={'page_id': self.pk})


class Contact(models.Model):
    seo = models.ForeignKey(SeoBlock, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    active = models.BooleanField(default=False)


class CinemaContact(models.Model):
    name = models.CharField(max_length=300)
    address = models.TextField()
    location = models.URLField(max_length=1000)
    logo = models.ImageField(upload_to='images/pages/', null=True, verbose_name='')


class MailingTemplate(models.Model):
    html_template = models.FileField(upload_to='mailing/', null=True, blank=True)


class Seance(models.Model):
    date = models.DateField(max_length=300, null=True)
    time = models.CharField(max_length=300, null=True)
    ticket_price = models.IntegerField(null=True)
    hall_id = models.IntegerField(null=True)
    film_id = models.IntegerField(null=True)
    cinema_id = models.IntegerField(null=True)
    type = models.CharField(max_length=10, null=True)
    film_name = models.CharField(max_length=300, null=True)
    hall_name = models.CharField(max_length=300, null=True)


class Ticket(models.Model):
    place = models.CharField(max_length=30, null=True)
    user = models.IntegerField(null=True)
    seance = models.IntegerField(null=True)
    reserve = models.BooleanField(default=False)
    sell = models.BooleanField(default=False)
    date = models.DateField(null=True)
    class Meta:
        unique_together = [['place', 'seance']]



