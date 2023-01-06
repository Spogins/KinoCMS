from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    address = models.CharField(max_length=300, null=True)
    card_number = models.CharField(max_length=50, null=True)
    language = models.CharField(max_length=10, null=True)
    gender = models.CharField(max_length=10, default=True)
    phone_number = models.CharField(max_length=50, null=True)
    birth_date = models.DateField(null=True)
    city = models.CharField(max_length=100, null=True)

    # class Meta:
    #     unique_together = [['username'], ['phone_number'], ['email']]

