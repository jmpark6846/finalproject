# -*- coding: utf-8 -*-
from django.shortcuts import render
from serializers import NewsSerializer, UserSerializer, WordsSerializer, CompanySerializer
from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from models import Company, News, getTodayNews
from word.models import Words, getTodayWords
from django import forms
import wordgram
import getNews
import json
from forms import LoginForm


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-date')
    serializer_class = NewsSerializer
    permissions_class = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WordsViewSet(viewsets.ModelViewSet):
    queryset = Words.objects.all().order_by('-freq')
    serializer_class = WordsSerializer
    permissions_class = (permissions.IsAuthenticatedOrReadOnly,)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


def index(request):
    hot_keywords = getTodayWords().order_by('-freq')[0:3]
    latest_news = getTodayNews().order_by('-id')[0:5]
    content = {
        'keywords': hot_keywords,
        'latest_n': latest_news
    }
    # todayWords = getTodayWords().order_by('-freq')[0:3]
    # latest_news = getTodayNews().order_by('-id')[0:5]
    # content={
    # 	'woee':todayWords,
    # 	'len':latest_news
    # }

    return render(request, 'index.html', content)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(username=email, password=password)

            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError("이메일과 비밀번호를 확인하세요.")

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


@login_required
def make_companies(request):
    Company.objects.create(
        name="동아일보",
        tend="보수"
    )
    Company.objects.create(
        name="중앙일보",
        tend="보수"
    )
    Company.objects.create(
        name="국민일보",
        tend="보수"
    )
    Company.objects.create(
        name="조선일보",
        tend="보수"
    )
    Company.objects.create(
        name="한겨례",
        tend="진보"
    )
    Company.objects.create(
        name="프레시안",
        tend="진보"
    )
    Company.objects.create(
        name="오마이뉴스",
        tend="진보"
    )
    Company.objects.create(
        name="경향신문",
        tend="진보"
    )
    return HttpResponseRedirect('/')


@login_required
def crawl_news(request):
    getNews.crawlNews_chosun(request.user)
    print "end chosun"
    getNews.crawlNews_joongang(request.user)
    print "end joongang"
    getNews.crawlNews_ohmynews(request.user)
    print "end ohmynews"
    getNews.crawlNews_hani(request.user)
    print "end hani"
    getNews.crawlNews_pressian(request.user)
    print "end pressian"
    getNews.crawlNews_donga(request.user)
    print "end donga"
    getNews.crawlNews_km(request.user)
    print "end km"
    getNews.crawlNews_seoul(request.user)
    print "end seoul"
    getNews.crawlNews_hankook(request.user)
    print "end hankook"

    return HttpResponseRedirect(reverse('keyword:words_list'))


@login_required
def delete_todaynews(request):
    getTodayNews().delete()
    return HttpResponseRedirect(reverse('keyword:words_list'))


@login_required
def analyze_news(request):
    print "start hannanum_analyze_22"
    analyzed_dics = wordgram.hannanum_analyze_22()
    print "end hannanum_analyze_22"
    wordgram.create_words(analyzed_dics)
    print "end create words"
    today_words = getTodayWords().order_by('-freq')

    for index, word in enumerate(today_words):
        word.rank = index + 1
        word.save()

    return HttpResponseRedirect(reverse('keyword:words_list'))
