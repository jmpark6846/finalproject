from django.conf.urls import include, url
from django.contrib import admin
import views
urlpatterns = [
    url(r'^$', views.words_list, name='words_list'),
    url(r'^delete/today_words/$', views.delete_todaywords, name='delete_todaywords'),
    url(r'^(?P<id>\d+)/$', views.words_detail, name='words_detail'),
    url(r'^get_words/$', views.get_words, name='get_words'),
    url(r'^(?P<word_id>\d+)/likes/(?P<news_id>\d+)/$', views.like_news, name='like_news'),
    url(r'^(?P<word_id>\d+)/dislikes/(?P<news_id>\d+)/$', views.dislike_news, name='dislike_news'),
    url(r'^get_chart_series/(?P<value>\w+)/$', views.get_chart_series, name='get_chart_series'),
]