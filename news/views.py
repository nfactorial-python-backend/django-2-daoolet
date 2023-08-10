from django.shortcuts import render, HttpResponse

from .models import News

# Create your views here.
def index(request):
    all_news = News.objects.all()
    context = {"news": all_news}
    return HttpResponse(context)