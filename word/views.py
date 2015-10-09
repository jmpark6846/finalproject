# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from news.models import getTodayNews
from models import getTodayWords, Words
from news.models import Company, News
from project.settings import LIST_SIZE, CHART_DAYS

# Create your views here.


def words_list(request):
    news_size = len(getTodayNews())
    return render(request, 'words/words_list.html', {'news_size': news_size})


def words_detail(request, id):
    if request.method == 'GET':

        word = Words.objects.get(id=id)
        conserv_news = News.objects.none()
        prog_news = News.objects.none()
        neutral_news = News.objects.none()

        conserv_com = Company.objects.filter(tend='보수')
        prog_com = Company.objects.filter(tend='진보')
        neutral_com = Company.objects.filter(tend='중립')

        for c in conserv_com:
            conserv_news = conserv_news | word.news.filter(company=c)

        for c in prog_com:
            prog_news = prog_news | word.news.filter(company=c)

        for c in neutral_com:
            neutral_news = neutral_news | word.news.filter(company=c)

        context = {
            'word':word,
            'conserv_news':conserv_news,
            'prog_news':prog_news,
            'neutral_news':neutral_news,
        }
        return render(request, 'words/words_detail.html', context)





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

def get_words_diff(request):
    import json

    options = json.loads(request.GET.get('tend'));
    print options

    list =[]
    list_value={}
    for o in options:
        companies = Company.objects.filter(tend=o)
        for company in companies:
            today_news = company.get_today_news()
            for news in today_news:
                for word in news.words.all():
                    word_dict={}
                    word_dict['freq']=word.freq
                    word_dict['value']=word.value

                    if word.value in list_value.keys():
                        word_dict['tend']=list_value[word.value]
                        if o not in list[list.index(word_dict)]['tend']:
                            list[list.index(word_dict)]['tend'].append(o)
                            list_value[word.value].append(o)

                    else:
                        list_value[word.value]=[]
                        list_value[word.value].append(o)
                        word_dict['tend']=[]
                        word_dict['tend'].append(o)
                        list.append(word_dict)

    list.sort(key=lambda x: x['freq'], reverse=True)
    data = json.dumps(list[0:LIST_SIZE])

    return HttpResponse(data, content_type="application/json")


def get_chart_series(request, value):
    all_words = Words.objects.filter(value=value).order_by('date')

    if all_words.count() > CHART_DAYS:
        words = all_words[all_words.count()-CHART_DAYS:]
        conserv_news = [0] * CHART_DAYS
        prog_news = [0] * CHART_DAYS
        neutral_news = [0] * CHART_DAYS
    else:
        words = all_words
        conserv_news = [0] * all_words.count()
        prog_news = [0] * all_words.count()
        neutral_news = [0] * all_words.count()

    words_index = []


    for idx, word in enumerate(words):
        words_index.append(word.freq)

    for index, word in enumerate(words):

        conserv_com = Company.objects.filter(tend='보수')
        prog_com = Company.objects.filter(tend='진보')
        neutral_com = Company.objects.filter(tend='중립')

        for c in conserv_com:
            conserv_news[index] += word.news.filter(company=c).count()

        for c in prog_com:
            prog_news[index] += word.news.filter(company=c).count()

        for c in neutral_com:
            neutral_news[index] += word.news.filter(company=c).count()

    data_dic=[conserv_news, prog_news, neutral_news, words_index]

    import json
    data = json.dumps(data_dic)
    return HttpResponse(data, content_type="application/json")