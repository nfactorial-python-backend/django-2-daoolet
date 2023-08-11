from django.db import models

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def has_comments(self):
        return self.comments.exists()

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments")