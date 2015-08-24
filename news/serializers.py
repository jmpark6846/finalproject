from django.contrib.auth.models import User
from django.forms import widgets
from rest_framework import serializers
from rest_framework import permissions
from models import *


class NewsSerializer(serializers.HyperlinkedModelSerializer):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)  
	class Meta:
		model = News
		fields = ('user','title','content','url','link','type', 'date')

class WordsSerializer(serializers.HyperlinkedModelSerializer):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)  
	class Meta:
		model = Words
		fields = ('value','freq','news','tag','date')

class UserSerializer(serializers.HyperlinkedModelSerializer):
	news = serializers.HyperlinkedIdentityField(view_name='news-detail', many=True, read_only=True)
	class Meta:
		model = User
		fields = ('url','username','news')