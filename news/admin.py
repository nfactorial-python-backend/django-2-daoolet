from django.contrib import admin

from .models import News, Comment

# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 5

class AdminNews(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ["title", "content", "created_at", "has_comments"]
    list_filter = ["created_at"]


admin.site.register(News, AdminNews)