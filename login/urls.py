from django.urls import path
from .views import *

urlpatterns = [
    path('', login_user, name='login_user'),

    path('logout', logout_user, name='logout_user'),

]