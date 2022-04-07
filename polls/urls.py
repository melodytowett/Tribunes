from django.conf import settings
from django.urls import path,re_path,include
from django.conf.urls.static import static
from . import views
from django_registration.backends.one_step.views import RegistrationView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path('',views.index, name='index'),
    path('',views.news_today,name='newsToday'),
    path('search/',views.search_results,name='search_results'),
    re_path(r'^archives/(\d{4}-\d{2}-\d{2})/$',views.past_days_news, name= 'pastNews'),
    path('article/(\d+)',views.article,name = 'article'),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path('accounts/register/',RegistrationView.as_view(success_url='/profile/'),name='django_registration_register'),
    path('ajax/newsletter/',views.newsletter,name='newsletter'),
    re_path(r'^api/merch/$',views.MerchList.as_view()),
    re_path(r'^api-token-auth/', obtain_auth_token),
    path('new/article', views.new_article, name='new-article'),
    re_path(r'api/merch/merch-id/(?P<pk>[0-9]+)/',views.MerchDescription.as_view())
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)