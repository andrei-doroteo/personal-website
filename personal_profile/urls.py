from django.urls import path

from personal_profile import views

app_name = "personal_profile"

urlpatterns = [
    path("", views.home, name="home"),
]
