from cgi import test
from django.test import TestCase
import datetime as dt
from polls.views import news_today
from .models import Editor,Article,tags
# Create your tests here.

class EditorTestClass(TestCase):
    def setUp(self):
        self.melody=Editor(first_name = 'Melody',last_name = 'Towett',email='melody@gmail.com')

    def test_instance(self):
        self.assertTrue(isinstance(self.melody,Editor))
    def test_save_method(self):
        self.melody.save_editor()
        editors = Editor.objects.all()
        self.assertTrue(len(editors) > 0)

class ArticleTestClass(TestCase):
    def setUp(self):
        self.melody=Editor(first_name = 'Melody',last_name='Towett',email='melody@gmail.com')
        self.melody.save_editor()

        self.new_tag = tags(name = 'testing')
        self.new_tag.save()
        self.new_article = Article(title = 'My Article',post = 'This is the first article',editor = self.melody)
        self.new_article.save()
        self.new_article.tags.add(self.new_tag)

    def tearDown(self):
        Editor.objects.all().delete()
        tags.objects.all().delete()
        Article.objects.all().delete()

    def test_get_news_today(self):
        today_news = Article.todays_news()
        self.assertTrue(len(today_news)>0)

    def test_get_news_by_date(self):
        test_date = '2021-11-11'
        date = dt.datetime.strptime(test_date,'%Y-%m-%d').date()
        news_by_date = Article.days_news(date)
        self.assertTrue(len(news_by_date) == 0)