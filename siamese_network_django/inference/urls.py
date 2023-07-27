from django.urls import path

from . import views

urlpatterns = [
    path("models/", views.getModels),
    path("search/", views.search),
    path("inference/", views.inference),
    path("addCarRim/", views.addCarRim),
    path("updateCarRim/", views.updateCarRim),
    path("deleteCarRim/", views.deleteCarRim),
    path("storedCarRimTypes/", views.storedCarRimTypes.as_view()),
    path("getCarRimTypeImages/", views.getCarRimTypeImages),
    path("storedCarRimTypesByCategory/", views.storedCarRimTypesByCategory.as_view()),
]