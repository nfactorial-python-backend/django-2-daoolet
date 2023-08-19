from django.urls import path

from . import views

app_name = "news"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:news_id>/", views.detail, name="detail"),
    path("add/", views.create_news, name="create_news"),
    path("<int:news_id>/edit/", views.UpdateNews.as_view(), name="update_news"),
    path("<int:news_id>/", views.UpdateNews.as_view(), name="updated_news"),
    path("<int:news_id>/delete/", views.delete_news, name="delete_news"),
    path("<int:news_id>/detail/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),
    path("api/news/", views.news_add, name="api_news_add"),
    path("api/news/<int:news_id>/", views.news_get, name="api_news_get"),
    path("api/news/<int:news_id>/delete", views.news_delete, name="api_news_delete"),
    path("api/news/list", views.news_get_list, name="api_news_list"),
]