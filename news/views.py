from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .models import News, Comment

# Create your views here.
def index(request):
    news = News.objects.all()
    context = {"news": news[::-1]}
    return render(request, "news/index.html", context)

def detail(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    if request.method == "POST":
        content = request.POST["content"]
        comment = Comment(content=content, news_id=news_id)
        comment.save()
        return HttpResponseRedirect(f"/news/{news.id}")
    
    coms = news.comments.all()
    context = {"news": news, "coms": coms[::-1]}
    return render(request, "news/detail.html", context)

def create_news(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        news = News(
            title=title,
            content=content,
        )
        news.save()
        return HttpResponseRedirect(f"/news/{news.id}")

    return render(request, "news/post_news.html")
