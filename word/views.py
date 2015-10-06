# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from news.models import getTodayNews
from models import getTodayWords, Words
from news.models import Company
from project.settings import LIST_SIZE

# Create your views here.


def words_list(request):
    news_size = len(getTodayNews())
    return render(request, 'words/words_list.html', {'news_size': news_size})


def words_detail(request, id):
    if request.method == 'GET':
        word = Words.objects.get(id=id)
        return render(request, 'words/words_detail.html', {'word': word, 'news_dic': news_dic})


def get_conserv_word(request):
    companies = Company.objects.filter(tend='보수')
    list =[]
    for company in companies:
        today_news = company.get_today_news()
        for news in today_news:
            for word in news.words.all():
                if word in list:
                    pass
                else:
                    list.append(word)

    list.sort(key=lambda x: x.freq, reverse=True)
    data = serializers.serialize("json", list[0:LIST_SIZE])
    return HttpResponse(data, content_type="application/json")


def get_prog_word(request):
    companies = Company.objects.filter(tend='진보')
    list =[]
    for company in companies:
        today_news = company.get_today_news()
        for news in today_news:
            for word in news.words.all():
                if word in list:
                    pass
                else:
                    list.append(word)

    list.sort(key=lambda x: x.freq, reverse=True)
    data = serializers.serialize("json", list[0:LIST_SIZE])
    return HttpResponse(data, content_type="application/json")

def get_words(request):
    import json
    options = json.loads(request.GET.get('tend'));
    print options
    list =[]
    for o in options:
        companies = Company.objects.filter(tend=o)
        print o
        print companies
        for company in companies:
            today_news = company.get_today_news()
            for news in today_news:
                for word in news.words.all():
                    if word in list:
                        pass
                    else:
                        list.append(word)

    list.sort(key=lambda x: x.freq, reverse=True)
    data = serializers.serialize("json", list[0:LIST_SIZE])

    return HttpResponse(data, content_type="application/json")