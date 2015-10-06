from django.conf.urls import include, url
from django.contrib import admin
import views
urlpatterns = [

    url(r'^analyze/$', views.analyze_news, name='news_analyze'),
    url(r'^crawl/$', views.crawl_news, name='crawl_news'),
    url(r'^delete/today/$', views.delete_todaynews, name='delete_todaynews'),
    
    
]