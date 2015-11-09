# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from news.models import getTodayNews
from news.models import Company, News
from project.settings import LIST_SIZE, CHART_DAYS, RECOMMEND_SIZE
from django.contrib.auth.decorators import login_required


@login_required
def users_mypage(request):
    likes = request.user.liked_news.order_by('-date')
    return render(request, 'mypage/mypage_liked.html', {'likes':likes})


def get_like_ratio(request):
    likes = request.user.liked_news.all()

    if len(likes) != 0:
        prog_n = 0.0
        conserv_n = 0.0

        for n in likes :
            if n.company.tend == u"진보":
                prog_n += 1
            else:
                conserv_n += 1

        prog_r = int((prog_n / (len(likes)) * RECOMMEND_SIZE) // 1)
        conserv_r = int((conserv_n / (len(likes)) * RECOMMEND_SIZE) // 1)
    else:
        prog_r = 5
        conserv_r = 5

    data_list=[conserv_r,prog_r]
    count=[conserv_n, prog_n]
    import json
    data = json.dumps({'data_list':data_list, 'count':count})
    return HttpResponse(data, content_type="application/json")



def get_news_ratio(user):
    likes = user.liked_news.all()

    if len(likes) != 0:
        prog_n = 0.0
        conserv_n = 0.0

        for n in likes :
            if n.company.tend == u"진보":
                prog_n += 1
            else:
                conserv_n += 1

        prog_r = int((prog_n / (len(likes)) * RECOMMEND_SIZE) // 1)
        conserv_r = int((conserv_n / (len(likes)) * RECOMMEND_SIZE) // 1)
    else:
        prog_r = 5
        conserv_r = 5

    return {'prog_r':prog_r, 'conserv_r':conserv_r}


def get_recommended_news(user):
    ratio = get_news_ratio(user)

    today_news = getTodayNews()

    conserv_com = Company.objects.filter(tend='보수')
    prog_com = Company.objects.filter(tend='진보')

    conserv_news = News.objects.none()
    prog_news = News.objects.none()

    for c in conserv_com:
        conserv_news = conserv_news | today_news.filter(company=c)
    conserv_news = sorted(conserv_news, key=lambda x: len(x.likes.all()), reverse=True)

    for c in prog_com:
        prog_news = prog_news | today_news.filter(company=c)
    prog_news = sorted(prog_news, key=lambda x: len(x.likes.all()), reverse=True)

    recom_news = conserv_news[:ratio['conserv_r']] + prog_news[:ratio['prog_r']]
    return recom_news


@login_required
def recommend_news(request):
    rec_news = get_recommended_news(request.user)
    return render(request, 'mypage/mypage_recommended.html', {'news':rec_news})


@login_required
def like_news_in_liked_page(request, id):
    news = News.objects.get(id=id)
    user = request.user

    if user in news.likes.all():
        news.likes.remove(user)

    elif user in news.dislikes.all():
        news.dislikes.remove(user)
        news.likes.add(user)
    else:
        news.likes.add(user)

    return HttpResponseRedirect(reverse('mypage:users_mypage'))


@login_required
def dislike_news_in_liked_page(request, id):
    news = News.objects.get(id=id)
    user = request.user

    if user in news.likes.all():
        news.likes.remove(user)
        news.dislikes.add(user)
    elif user in news.dislikes.all():
        news.dislikes.remove(user)
    else:
        news.dislikes.add(user)

    return HttpResponseRedirect(reverse('mypage:users_mypage'))

@login_required
def like_in_recommend_page(request, id):
    news = News.objects.get(id=id)
    user = request.user

    if user in news.likes.all():
        news.likes.remove(user)

    elif user in news.dislikes.all():
        news.dislikes.remove(user)
        news.likes.add(user)
    else:
        news.likes.add(user)

    return HttpResponseRedirect(reverse('mypage:recommend_news'))

@login_required
def dislike_in_recommend_page(request, id):
    news = News.objects.get(id=id)
    user = request.user

    if user in news.likes.all():
        news.likes.remove(user)
        news.dislikes.add(user)
    elif user in news.dislikes.all():
        news.dislikes.remove(user)
    else:
        news.dislikes.add(user)

    return HttpResponseRedirect(reverse('mypage:recommend_news'))
