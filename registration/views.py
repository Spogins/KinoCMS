from django.contrib.auth import login, authenticate
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.http.response import JsonResponse, HttpResponse
from users.forms import CustomUserCreationForm
from users.models import CustomUser
username_validator = ASCIIUsernameValidator()
# Create your views here


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def registration(request):
    if is_ajax(request):
        form = CustomUserCreationForm(request.POST)
        if request.POST['email'] == '':
            form.errors['email'] = form.error_class(['Обязательное поле.'])

        if CustomUser.objects.filter(email=request.POST['email']):
            form.errors['email'] = form.error_class(['Email уже зарегистрирован.'])

        if CustomUser.objects.filter(username=request.POST['username']):
            form.errors['username'] = form.error_class(['Имя пользователя уже занято.'])

        if request.POST['username'] != '' and len(request.POST['username']) < 5:
            form.errors['username'] = form.error_class(['Имя пользователя слишком короткое.'])

        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            password = request.POST.get('password2')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return JsonResponse({'user': 'succes'})
        else:
            return JsonResponse(form.errors)
    return JsonResponse({'errors': 'no_errors_list'})

