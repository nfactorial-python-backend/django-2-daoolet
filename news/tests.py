from django.test import TestCase
from django.urls import reverse
from django.utils import timezone


from .models import News, Comment
# Create your tests here.

class NewsModelTests(TestCase):
    def test_has_comments_true(self):
        news = News(title="Test News", content="Test News")
        news.save()
        comment = Comment(content="Test Comment", news=news)
        comment.save()
        self.assertTrue(news.has_comments())

    def test_has_comments_false(self):
        news = News(title="Test no comments", content="Test no comments")
        news.save()
        self.assertFalse(news.has_comments())

        
class NewsViewTests(TestCase):
    def test_index(self):
        n1 = News(title="CNN NEWS", content="CNN NEWS")
        n2 = News(title="BBC NEWS", content="BBC NEWS")
        n3 = News(title="KAZ NEWS", content="KAZ NEWS")

        n1.save()
        n2.save()
        n3.save()

        response = self.client.get(reverse("news:index"))

        self.assertIs(200, response.status_code)
        self.assertQuerysetEqual([n3, n2, n1], response.context["news"])

    def test_detail_news(self):
        n1 = News(title="CNN NEWS", content="CNN NEWS")
        created_at = timezone.now()
        n1.save()

        url = reverse("news:detail", args=(n1.id, ))
        expected_url = f"/news/102/{n1.id}/"
        self.assertEqual(url, expected_url)

        response = self.client.get(reverse("news:detail", args=(n1.id, )))

        self.assertIs(200, response.status_code)
        self.assertContains(response, n1.title)
        self.assertContains(response, n1.content)
        self.assertFalse(n1.has_comments())
        self.assertEqual(created_at, n1.created_at)


    def test_detail_comments(self):
        n1 = News(title="Test News", content="Test News")
        n1.save()

        c1 = Comment(content="Test Comment1", news=n1)
        c2 = Comment(content="Test Comment2", news=n1)
        c3 = Comment(content="Test Comment3", news=n1)

        c1.save()
        c2.save()
        c3.save()

        response = self.client.get(reverse("news:detail", args=(n1.id, )))

        self.assertIs(200, response.status_code)
        self.assertQuerysetEqual([c3, c2, c1], response.context["coms"])

