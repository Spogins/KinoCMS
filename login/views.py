from django.contrib.auth import authenticate, login, logout
from django.http.response import JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def login_user(request):
    if is_ajax(request):
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '' or password == '':
            return JsonResponse({'password1': 'Заполните все поля'})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'user': username})
        else:
            return JsonResponse({'password1': 'Не верный имя пользователя или пароль'})


def logout_user(request):
    if request.user.is_superuser:
        logout(request)
        return redirect(f'/admin_page')
    else:
        logout(request)
        return redirect(f'/')

