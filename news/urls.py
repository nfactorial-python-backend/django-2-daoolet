from django.urls import path

from . import views

app_name = "news"
urlpatterns = [
    path("", views.index, name="index"),
    path("102/<int:news_id>/", views.detail, name="detail"),
    path("add/", views.create_news, name="create_news"),
]