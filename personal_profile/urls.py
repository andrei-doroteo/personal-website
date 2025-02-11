from django.urls import path

from personal_profile import views

urlpatterns = [
    path("", views.home, name="home"),
]
