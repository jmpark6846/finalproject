from django.conf.urls import include, url
from django.contrib import admin
import views
urlpatterns = [
    url(r'^$', views.words_list, name='words_list'),
    url(r'^(?P<id>\d+)/$', views.words_detail, name='words_detail'),
    url(r'^conserv_word/$', views.get_conserv_word, name='conserv_word'),
    url(r'^prog_word/$', views.get_prog_word, name='prog_word'),
    url(r'^all_word/$', views.get_all_word, name='all_word'),
]