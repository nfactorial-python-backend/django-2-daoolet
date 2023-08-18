from django.urls import path

from . import views

app_name = "news"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:news_id>/", views.detail, name="detail"),
    path("add/", views.create_news, name="create_news"),
    path("<int:news_id>/edit/", views.UpdateNews.as_view(), name="update_news"),
    path("<int:news_id>/", views.UpdateNews.as_view(), name="updated_news"),
    path("<int:news_id>/delete", views.delete_news, name="delete_news"),
    path("<int:comment_id>/delete", views.delete_comment, name="delete_comment")
]