# -*- coding: utf-8 -*-
from django.shortcuts import render
from serializers import NewsSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import HttpResponseRedirect, HttpResponse
from models import News
import getNews
import json

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

def news(request):
	news_db = getNews.getNews("http://www.ytn.co.kr/news/news_list_0101.html")
	json_news_db = json.dumps(news_db)
	
	return HttpResponse(json_data,content_type="application/json")
