# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from news.models import getTodayNews
from models import getTodayWords, Words, getWordsAt
from rest_framework.reverse import reverse
from news.models import Company, News
from project.settings import LIST_SIZE, CHART_DAYS
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def delete_todaywords(request):
    getTodayWords().delete()
    return HttpResponseRedirect(reverse('keyword:words_list'))


def words_list(request):
    news_size = len(getTodayNews())
    words_size = len(getTodayWords())
    recent_words_lists=[]
    import datetime
    for i in range(0,3):
        date = datetime.datetime.now() - datetime.timedelta(days=i)
        words=getWordsAt(date)
        recent_words_lists.append(words[:10])
    date = datetime.datetime.now()

    context = {'news_size': news_size,
               'words_size':words_size,
               'recent_words_lists':recent_words_lists,
               'date':date
    }
    return render(request, 'words/words_list.html', context)


def words_detail(request, id):
    if request.method == 'GET':

        word = Words.objects.get(id=id)
        recent_words = Words.objects.filter(value=word.value).order_by('-date')[:CHART_DAYS]
        conserv_news = News.objects.none()
        prog_news = News.objects.none()
        # neutral_news = News.objects.none()

        conserv_com = Company.objects.filter(tend='보수')
        prog_com = Company.objects.filter(tend='진보')
        # neutral_com = Company.objects.filter(tend='중립')

        for c in conserv_com:
            conserv_news = conserv_news | word.news.filter(company=c)
        conserv_news = sorted(conserv_news, key=lambda x: len(x.likes.all()), reverse=True)

        for c in prog_com:
            prog_news = prog_news | word.news.filter(company=c)
        prog_news = sorted(prog_news, key=lambda x: len(x.likes.all()), reverse=True)

        # for c in neutral_com:
        #     neutral_news = neutral_news | word.news.filter(company=c)
        # neutral_news = sorted(neutral_news, key=lambda x: len(x.likes.all()), reverse=True)

        context = {
            'word':word,
            'recent_words':recent_words,
            'conserv_news':conserv_news,
            'prog_news':prog_news,
            # 'neutral_news':neutral_news,
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


# datetime format을 json으로 변환하기 위한 핸들러
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def get_chart_series(request, value):
    all_words = Words.objects.filter(value=value).order_by('date')

    if all_words.count() > CHART_DAYS:
        words = all_words[all_words.count()-CHART_DAYS:]
        conserv_news = [0] * CHART_DAYS
        prog_news = [0] * CHART_DAYS
    else:
        words = all_words
        conserv_news = [0] * all_words.count()
        prog_news = [0] * all_words.count()

    words_index = []
    words_date = []
    import datetime

    for idx, word in enumerate(words):
        words_index.append(word.freq)
        date = word.date + datetime.timedelta(days=1)
        words_date.append(date.strftime("%m/%d"))

    for index, word in enumerate(words):
        conserv_com = Company.objects.filter(tend='보수')
        prog_com = Company.objects.filter(tend='진보')

        for c in conserv_com:
            conserv_news[index] += word.news.filter(company=c).count()

        for c in prog_com:
            prog_news[index] += word.news.filter(company=c).count()

    data_list=[conserv_news, prog_news, words_index]

    import json
    data = json.dumps({'data_list':data_list, 'words_date':words_date},default=date_handler)
    return HttpResponse(data, content_type="application/json")


def order_news_by_like(word_id):
    word = Words.objects.get(id=word_id)

    conserv_news = News.objects.none()
    prog_news = News.objects.none()

    prog_com = Company.objects.filter(tend='진보')
    for c in prog_com:
        prog_news = prog_news | word.news.filter(company=c)

    prog_news = sorted(prog_news, key=lambda x: len(x.likes.all()), reverse=True)


    conserv_com = Company.objects.filter(tend='보수')
    for c in conserv_com:
        conserv_news = conserv_news | word.news.filter(company=c)
    conserv_news = sorted(conserv_news, key=lambda x: len(x.likes.all()), reverse=True)

    context ={'prog_news':prog_news, 'conserv_news':conserv_news}
    return context


@login_required
def like_news_in_words_detail(request, word_id, news_id):
    user = request.user
    news = News.objects.get(id=news_id)

    if user in news.likes.all():
        news.likes.remove(user)

    elif user in news.dislikes.all():
        news.dislikes.remove(user)
        news.likes.add(user)
    else:
        news.likes.add(user)

    context = order_news_by_like(word_id)

    return render(request, 'words/news_list_in_word_details.html', context)


@login_required
def dislike_news_in_words_detail(request, word_id, news_id):
    user = request.user
    news = News.objects.get(id=news_id)

    if user in news.likes.all():
        news.likes.remove(user)
        news.dislikes.add(user)
    elif user in news.dislikes.all():
        news.dislikes.remove(user)
    else:
        news.dislikes.add(user)

    context = order_news_by_like(word_id)
    return render(request, 'words/news_list_in_word_details.html', context)


@login_required
def like_news(request, news_id):
    user = request.user
    news = News.objects.get(id=news_id)

    if user in news.likes.all():
        news.likes.remove(user)

    elif user in news.dislikes.all():
        news.dislikes.remove(user)
        news.likes.add(user)
    else:
        news.likes.add(user)

    return HttpResponse('liked!');

@login_required
def dislike_news(request, news_id):
    user = request.user
    news = News.objects.get(id=news_id)

    if user in news.likes.all():
        news.likes.remove(user)
        news.dislikes.add(user)
    elif user in news.dislikes.all():
        news.dislikes.remove(user)
    else:
        news.dislikes.add(user)

    return HttpResponse('disliked!');