# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from konlpy.tag import Hannanum
from operator import itemgetter
from konlpy.utils import pprint
from collections import OrderedDict, Counter
from datetime import datetime
from models import *
from tfidf import tf_idf_map
import os

from os import listdir

# 문장부호제거
def remove_puc_marks(contents):
	pmarks=['】','【','▲','ⓒ','·','\'','\"','?', '/', '(', ')','[',']', ',', '.', ':', '{', '}', ';', '!', '@', '#', '$', '%', '^', '&', '-', '_', '=', '<', '>', '*','\n', '\r']
	pmarks_special=[]
	for mark in pmarks:
		if type(contents) == str :
			contents= contents.replace(mark,' ')
		else:
			contents= contents.replace(mark.decode('utf8'),' ')
	return contents


# 불용어 제거
def remove_stopwords(dictionary):
	file = open('news/stopwords.txt','r')
	stopwords = file.readlines()

	for stopword in stopwords:
		sw = stopword.replace('\n','')	
		if sw.decode('utf8') in dictionary:
			del dictionary[sw.decode('utf8')]

	return dictionary


# 한나눔 22품사 분류
def hannanum_analyze_22():
	
	h= Hannanum()
	tags={
		'NC':'보통명사',
		'NQ':'고유명사',
	}	
	"""
	pos_dics=
	{
		news.id : dictionary,
		news.id : dictionary,
	}
	"""
	pos_dics = {}
	news = getTodayNews()
	
	for n in news :
		# 뉴스내용으로 품사 분석해서 딕셔너리로 반환
		n.content = remove_puc_marks(n.content)
		words_dic = h.pos(n.content,22)
		dictionary={}
		for t in words_dic:
			word = t[0]
			key = t[1]
			if key in tags.keys():
				if not word in dictionary.keys():
					dictionary[word] =1
				else :
					dictionary[word] +=1

		dictionary=remove_stopwords(dictionary)	# 불용어 제거
		pos_dics[n]=dictionary

	# tfidf
	print "tf-idf"
	analyzed_dics=tf_idf_map(pos_dics)

	return analyzed_dics

	# dictionary=Counter(dictionary).most_common(5)
	# 각 뉴스별 단어 딕셔너리를 디비에 추가한다.


def create_words(analyzed_dics):
	dic = {}
	"""
	dic=
	{
		단어 : [뉴스,뉴스,],
	}
	"""
	for news,data in analyzed_dics.items():
		sorted_data = Counter(data).most_common(30)

		for item in sorted_data:
			keyword=item[0]
			if keyword not in dic:
				dic[keyword]=[news]
			else:
				dic[keyword].append(news)

	for keyword, news_list in dic.items():
		if len(news_list) <= 3 :
			continue
		else:
			word=Words.objects.create(
				value=keyword,
				freq=len(news_list),
				date=datetime.now().strftime('%Y-%m-%d'),
			)
			for n in news_list:
				word.news.add(n)
