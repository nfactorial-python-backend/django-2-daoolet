from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View


from .models import News, Comment
from .forms import NewsForm

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
        return HttpResponseRedirect(reverse("news:detail", args=(news_id,)))
    
    coms = news.comments.all()
    context = {"news": news, "coms": coms[::-1]}
    return render(request, "news/detail.html", context)

def create_news(request):
    if request.method == "POST":
        create_form = NewsForm(request.POST)
        if create_form.is_valid():
            news = create_form.save()

        return HttpResponseRedirect(reverse("news:detail", args=(news.id, )))

    return render(request, "news/post_news.html")


class UpdateNews(View):

    def get(self, request, news_id):
        current_news = get_object_or_404(News, pk=news_id)
        update_form = NewsForm(instance=current_news)
        return render(request, "news/update_news.html", {"update_form": update_form})

    def post(self, request, news_id):
        updated_news = get_object_or_404(News, pk=news_id)
        updated_form = NewsForm(request.POST, instance=updated_news)

        if updated_form.is_valid():
            updated_form.save()

        return HttpResponseRedirect(reverse("news:detail", args=(news_id,)))