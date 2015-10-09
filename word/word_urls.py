from django.conf.urls import include, url
from django.contrib import admin
import views
urlpatterns = [
    url(r'^$', views.words_list, name='words_list'),
    url(r'^(?P<id>\d+)/$', views.words_detail, name='words_detail'),
    url(r'^get_words/$', views.get_words, name='get_words'),
    url(r'^get_chart_series/(?P<value>\w+)/$', views.get_chart_series, name='get_chart_series'),
]