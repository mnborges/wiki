from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name ="search"),
    path("new", views.newpage, name = "newpage"), 
    path("random", views.randpage, name="random"),
    path("<str:title>", views.item, name ="item"),
    path("<str:title>/edit", views.edit, name="edit")
]
