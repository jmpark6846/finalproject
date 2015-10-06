from django.contrib.auth.models import User
from django.forms import widgets
from rest_framework import serializers
from rest_framework import permissions
from models import *
from word.models import Words

class CompanySerializer(serializers.HyperlinkedModelSerializer):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)  
	news = serializers.HyperlinkedIdentityField(view_name='news-detail', many=True, read_only=True)
	class Meta:
		model = Company
		fields = ('name','news','tend')

class NewsSerializer(serializers.HyperlinkedModelSerializer):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)  
	class Meta:
		model = News
		fields = ('id','user','title','content','url','link','type', 'date', 'company' ,'words')

class WordsSerializer(serializers.HyperlinkedModelSerializer):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)  
	class Meta:
		model = Words
		fields = ('id','value','freq','news','tag','date')

class UserSerializer(serializers.HyperlinkedModelSerializer):
	news = serializers.HyperlinkedIdentityField(view_name='news-detail', many=True, read_only=True)
	class Meta:
		model = User
		fields = ('url','username','news')