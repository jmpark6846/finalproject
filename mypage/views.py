# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from news.models import getTodayNews
from news.models import Company, News, NewsLikes, NewsDislikes
from project.settings import LIST_SIZE, CHART_DAYS, RECOMMEND_SIZE
from django.contrib.auth.decorators import login_required


@login_required
def users_mypage(request):
    likes = NewsLikes.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'mypage/mypage_liked.html', {'likes':likes})


def get_recommended_news(user):
    likes = NewsLikes.objects.filter(user=user)

    prog_n = 0.0
    conserv_n = 0.0

    prog_r = 0.0
    conserv_r = 0.0

    for l in likes:
        if l.news.company.tend == u"보수":
            conserv_n += 1
        else:
            prog_n += 1

    prog_r = int((prog_n / (prog_n + conserv_n) * RECOMMEND_SIZE) // 1)
    conserv_r = int((conserv_n / (prog_n + conserv_n) * RECOMMEND_SIZE) // 1)

    today_news = getTodayNews()

    conserv_com = Company.objects.filter(tend='보수')
    prog_com = Company.objects.filter(tend='진보')

    conserv_news = News.objects.none()
    prog_news = News.objects.none()
    recom_news = News.objects.none()

    for c in conserv_com:
        conserv_news = conserv_news | today_news.filter(company=c)
    conserv_news = sorted(conserv_news, key=lambda x: x.likes, reverse=True)

    for c in prog_com:
        prog_news = prog_news | today_news.filter(company=c)
    prog_news = sorted(prog_news, key=lambda x: x.likes, reverse=True)

    recom_news = conserv_news[:conserv_r] + prog_news[:prog_r]
    return recom_news


@login_required
def recommend_news(request):
    rec_news = get_recommended_news(request.user)

    import random
    random.shuffle(rec_news)
    return render(request, 'mypage/mypage_recommended.html', {'news':rec_news})


def get_liked_ratio_data(request):
    likes = NewsLikes.objects.filter(user=request.user)

    prog_n = 0.0
    conserv_n = 0.0

    for l in likes:
        if l.news.company.tend == u"보수":
            conserv_n += 1
        else:
            prog_n += 1

    data_list = [conserv_n,prog_n]
    import json
    data = json.dumps(data_list)
    return HttpResponse(data, content_type="application/json")