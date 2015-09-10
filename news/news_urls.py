from django.conf.urls import include, url
from django.contrib import admin
import views
urlpatterns = [

    url(r'^$',views.words_list, name='words_list'),
    url(r'^(?P<id>\d+)/$',views.words_detail, name='words_detail'),
    url(r'^analyze/$', views.analyze_news, name='news_analyze'),
    url(r'^crawl/$', views.crawl_news, name='crawl_news'),
    url(r'^delete/today/$', views.delete_todaynews, name='delete_todaynews'),
    
    
]