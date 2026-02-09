
from django import forms
from django.contrib.auth import get_user_model


class LoginUserForm(forms.Form):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль',widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')