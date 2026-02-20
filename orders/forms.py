from django import forms


class OrderCreateForm(forms.Form):
    """Форма оформления заказа"""
    
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличными при получении"),
        ("card", "Картой при получении"),
        ("online", "Онлайн оплата"),
    ]
    
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Имя"
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Фамилия"
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Email"
        })
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "placeholder": "Телефон"
        })
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 3,
            "placeholder": "Адрес доставки"
        })
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Город"
        })
    )
    postal_code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "placeholder": "Почтовый индекс"
        })
    )
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES
    )
    delivery_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "rows": 2,
            "placeholder": "Примечания к доставке"
        })
    )
