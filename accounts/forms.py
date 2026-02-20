from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя"""
    
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        "placeholder": "Email"
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Имя пользователя"
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Пароль"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Подтверждение пароля"
    }))
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    """Форма редактирования профиля"""
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "address", "city", "postal_code"]
        widgets = {
            "first_name": forms.TextInput(attrs={}),
            "last_name": forms.TextInput(attrs={}),
            "email": forms.EmailInput(attrs={}),
            "phone": forms.TextInput(attrs={}),
            "address": forms.Textarea(attrs={"rows": 3}),
            "city": forms.TextInput(attrs={}),
            "postal_code": forms.TextInput(attrs={}),
        }
