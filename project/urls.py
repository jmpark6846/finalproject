from django.conf.urls import url, include  
from rest_framework.routers import DefaultRouter
from news import news_urls, views
from word import word_urls
from mypage import users_urls

from django.contrib import admin
import settings

router = DefaultRouter()
router.register(r'news', views.NewsViewSet)
router.register(r'mypage', views.UserViewSet)
router.register(r'words', views.WordsViewSet)
router.register(r'company', views.CompanyViewSet)

urlpatterns = [
    # setting
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest-api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # sessions
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),

    # apps
    url(r'^news/', include(news_urls, namespace='news')),
    url(r'^keyword/', include(word_urls, namespace='keyword')),
    url(r'^mypage/', include(users_urls, namespace='mypage')),
    url(r'^company/make', views.make_companies, name='make_companies'),

]
