from django.conf.urls import include, url
from django.contrib import admin
import views
urlpatterns = [
    url(r'^(?P<id>\d+)/$', views.news_detail, name='news_detail'),
    url(r'^analyze/$', views.analyze_news, name='news_analyze'),
    url(r'^crawl/$', views.crawl_news, name='crawl_news'),
    url(r'^delete/today/$', views.delete_todaynews, name='delete_todaynews'),
    url(r'^like_news_in_news_detail/(?P<id>\d+)/$', views.like_news_in_news_detail, name='like_news_in_news_detail'),
    url(r'^dislike_news_in_news_detail/(?P<id>\d+)/$', views.dislike_news_in_news_detail, name='dislike_news_in_news_detail'),
    url(r'^example/$', views.example, name='example'),
]