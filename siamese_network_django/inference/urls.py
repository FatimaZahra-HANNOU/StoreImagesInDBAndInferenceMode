from django.urls import path

from . import views

urlpatterns = [
    path("storedCarRimTypes/", views.storedCarRimTypes.as_view()),
    path("inference/", views.inference),
]