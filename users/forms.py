from django.forms import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser


GENDERS = (
        ('male', 'Мужчина'),
        ('female', 'Женщина')
    )
LANGUAGES = (
    ('ru', 'Русский'),
    ('uk', 'Украинский')
)


class CustomUserCreationForm(UserCreationForm):
    password2 = CharField(
        widget=PasswordInput(attrs={
            'type': 'password',
            'class': 'form-control',
            'autocomplete': "off",
            'placeholder': 'Пароль...'})
    )
    password1 = CharField(
        widget=PasswordInput(attrs={
            'type': 'password',
            'class': 'form-control',
            'autocomplete': "off",
            'placeholder': 'Подтвердить пароль...'})
    )

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')
        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Никнейм...'
            }),

            "email": EmailInput(attrs={
                'class': 'form-control',
                'type': 'email',
                'placeholder': 'Email...',
                'autocomplete': "username email",
            }),
            # "password1": PasswordInput(attrs={
            #     'type': 'password',
            #     'class': 'form-control',
            #     'placeholder': 'Пароль...'}),
            # "password2": PasswordInput(attrs={
            #     'type': 'password',
            #     'class': 'form-control',
            #     'placeholder': 'Подтвердить пароль...'}),
        }


class CustomUserChangeForm(UserChangeForm):
    password = CharField(max_length=30, required=False, widget=PasswordInput(attrs={
        'id': 'password',
        'class': 'form-control',
        'placeholder': 'Пароль...'
    }))
    r_password = CharField(max_length=30, required=False, widget=PasswordInput(attrs={
        'id': 'confirm_password',
        'class': 'form-control',
        'placeholder': 'Подтвердить пароль...',
    }))

    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'last_name', 'username', 'email', 'address', 'card_number', 'language', 'gender',
            'phone_number',
            'birth_date', 'city')
        widgets = {
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'type': 'text'}),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'type': 'text'}),
            'username': TextInput(attrs={
                'class': 'form-control',
                'type': 'text'}),
            'email': EmailInput(attrs={
                'class': 'form-control',
                'type': 'email'}),
            'address': TextInput(attrs={
                'class': 'form-control',
                'type': 'text'}),
            'card_number': TextInput(attrs={
                'class': 'form-control',
                'type': 'text'}),
            'language': Select(attrs={'class': 'form-select'}, choices=LANGUAGES),
            'gender': Select(attrs={'class': 'form-select'}, choices=GENDERS),
            'phone_number': TextInput(attrs={
                'class': 'form-control',
                'type': 'text'}),
            'birth_date': DateInput(attrs={
                'type': 'date',
            }, format='%Y-%m-%d'),
            'city': TextInput(attrs={
                'class': 'form-control',
                'type': 'text'}),
        }

    def clean(self):
        if self.cleaned_data['password'] != '' and self.cleaned_data['r_password'] != '':
            if self.cleaned_data['password'] != self.cleaned_data['r_password']:
                msg = 'Пароли не совпадают!'
                self._errors['password'] = self.error_class([msg])
                self._errors['r_password'] = self.error_class([msg])
                raise ValidationError(msg)
            else:
                validate_password(self.cleaned_data['password'])
        else:
            return self.cleaned_data


class NewUserForm(UserCreationForm):
    password = CharField(max_length=30, required=False, widget=PasswordInput(attrs={
        'id': 'password',
        'class': 'form-control',
        'placeholder': 'Пароль...'
    }))
    r_password = CharField(max_length=30, required=False, widget=PasswordInput(attrs={
        'id': 'confirm_password',
        'class': 'form-control',
        'placeholder': 'Подтвердить пароль...',
    }))

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control',
                'type': 'text'}),
            "email": EmailInput(attrs={
                'class': 'form-control',
                'type': 'email'}),
            "password1": PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль...'}),
            "password2": PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Подтвердить пароль...'}),
        }

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


