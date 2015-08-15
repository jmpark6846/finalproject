# -*- coding: utf-8 -*-
from django.shortcuts import render
from serializers import NewsSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from models import News
from django import forms
import wordgram
import getNews
import json
from forms import LoginForm

class NewsViewSet(viewsets.ModelViewSet):
	queryset = News.objects.all()
	serializer_class = NewsSerializer
	permissions_class = (permissions.IsAuthenticatedOrReadOnly,)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

def index(request):
	return render(request, 'index.html')

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

	return render(request, 'login.html', {'form' : form})

@login_required
def logout(request):
	auth_logout(request)
	return HttpResponseRedirect('/')

@login_required
def analyze_news(request):
	getNews.crawlNews(request.user, "http://www.ytn.co.kr/news/news_list_0101.html")
	contents = getNews.addAllTodayNews()
	analyzed_words = wordgram.hannanum_analyze_22(contents)
	result = wordgram.addup(analyzed_words)
	wordgram.print_dict(result)
	return HttpResponse("success")


