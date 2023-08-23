from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import News, Comment
from .forms import NewsForm, SignUpForm, CommentForm
from .serializers import NewsSerializer

# Create your views here.

@api_view(["POST"])
def news_add(request):
    serializer = NewsSerializer(data=request.data)
    if serializer.is_valid():
        news = serializer.save(commit=False)
        news.author = request.user
        news.save()
        return Response({"detail": "Successful added", "news_id": news.id})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def news_get(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    serializer = NewsSerializer(news)
    return Response(serializer.data)

@api_view(["DELETE"])
def news_delete(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    news.delete()
    return Response("Successful deleted", status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
def news_get_list(request):
    news = News.objects.all()
    serializer = NewsSerializer(news, many=True)    
    return Response(serializer.data)

def index(request):
    news = News.objects.all()
    context = {"news": news[::-1]}
    return render(request, "news/index.html", context)

# @permission_required("news.add_comments", login_url="/login")
def detail(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.news_id = news_id
        comment.author = request.user
        comment.save()
        return HttpResponseRedirect(reverse("news:detail", args=(news_id,)))
    
    coms = news.comments.all()
    context = {"news": news, "coms": coms[::-1]}
    return render(request, "news/detail.html", context)

@login_required(login_url="/login")
@permission_required("news.add_news", login_url="/login")
def create_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            # print(request.user)
            news.save()
            return HttpResponseRedirect(reverse("news:detail", args=(news.id, )))

    return render(request, "news/post_news.html")


class UpdateNews(View):

    def get(self, request, news_id):
        current_news = get_object_or_404(News, pk=news_id)
        update_form = NewsForm(instance=current_news)
        return render(request, "news/update_news.html", {"update_form": update_form})
    
    @permission_required("news.change_news", login_url="/login")
    def post(self, request, news_id):
        updated_news = get_object_or_404(News, pk=news_id)
        updated_form = NewsForm(request.POST, instance=updated_news)

        if updated_form.is_valid():
            updated_form.save()

        return HttpResponseRedirect(reverse("news:detail", args=(news_id,)))
    

def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            group = Group.objects.get(name="default")
            group.user_set.add(user)

            login(request, user)
            return redirect(reverse("news:index"))
    else:
        form = SignUpForm()
    
    return render(request, "registration/sign_up.html", {"form": form})

@permission_required("news.delete_news", login_url="/login")
def delete_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    if request.method == "POST":
        if request.user == news.author or request.user.has_perm("news.delete_news"):
            news.delete()
    
    return redirect(reverse("news:index"))


def delete_comment(request, news_id, comment_id):
    news = get_object_or_404(News, pk=news_id)
    coms = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        if request.user == coms.author or request.user.has_perm("comment.delete_comment"):
            coms.delete()
    return redirect(reverse("news:detail", args=(news.id, )))