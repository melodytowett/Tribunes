from django.conf import settings
from django.urls import path,re_path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('today/',views.news_today,name='newsToday'),
    path('search/',views.search_results,name='search_results'),
    re_path(r'^archives/(\d{4}-\d{2}-\d{2})/$',views.past_days_news, name= 'pastNews'),
    re_path(r'^articles/(\d+)',views.article,name = 'article'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)