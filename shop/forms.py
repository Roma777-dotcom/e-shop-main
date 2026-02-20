from django import forms
from .models import Product


class ProductFilterForm(forms.Form):
    """Форма фильтрации товаров"""
    
    SORT_CHOICES = [
        ("", "По умолчанию"),
        ("price_asc", "Цена: по возрастанию"),
        ("price_desc", "Цена: по убыванию"),
        ("name_asc", "Название: А-Я"),
        ("name_desc", "Название: Я-А"),
        ("newest", "Сначала новые"),
    ]
    
    min_price = forms.DecimalField(
        required=False, 
        widget=forms.NumberInput(attrs={
            "placeholder": "От"
        })
    )
    max_price = forms.DecimalField(
        required=False, 
        widget=forms.NumberInput(attrs={
            "placeholder": "До"
        })
    )
    sort = forms.ChoiceField(
        choices=SORT_CHOICES, 
        required=False
    )
