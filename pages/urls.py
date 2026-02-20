from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path("about/", views.about, name="about"),
    path("delivery/", views.delivery, name="delivery"),
    path("payment/", views.payment, name="payment"),
    path("contacts/", views.contacts, name="contacts"),
]
