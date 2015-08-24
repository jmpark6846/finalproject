# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from konlpy.tag import Hannanum
from operator import itemgetter
from konlpy.utils import pprint
from collections import OrderedDict, Counter
from datetime import datetime
from models import *
import os

from os import listdir

# 문장부호제거
def remove_puc_marks(contents):
	pmarks=['·','?', '\/', '(', ')', ',', '.', ':', '{', '}', ';', '!', '@', '#', '$', '%', '^', '&', '-', '_', '=', '<', '>', '*','\n', '\r']
	for mark in pmarks:
		contents= contents.replace(mark,' ')
	return contents

# 불용어 제거
def remove_stopwords(dictionary):
	file = open("stopwords.txt","r")
	stopwords = file.readlines()

	for stopword in stopwords:
		sw = stopword.replace('\n','')
		if sw in dictionary:
			del dictionary[sw]

	return dictionary

# 한나눔 22품사 분류
def hannanum_analyze_22():
	
	h= Hannanum()
	tags={
		'NC':'보통명사',
		'NQ':'고유명사',
	}	
	news = getTodayNews()
	for n in news : 
		# 뉴스내용으로 품사 분석해서 딕셔너리로 반환
		words_dic = h.pos(n.content,22)
		dictionary={}
		for t in words_dic:
			key = t[0]
			value = t[1]
			if value in tags.keys():
				# '먹' 같은 용언에는 '-다'를 붙여 '먹다' 같은 동사로 키값 사용
				if value.startswith("P"):
					key += u"다"

				if not key in dictionary.keys():
					dictionary[key] =1
				else :
					dictionary[key] +=1

		print n.title+" ("+str(len(dictionary))+")"
		# dictionary=remove_stopwords(dictionary)	# 불용어 제거
		dictionary=Counter(dictionary).most_common(5)

		# 각 뉴스별 단어 딕셔너리를 디비에 추가한다.
		for t in dictionary:
			key = t[0]
			value = t[1]
			todayWords = getTodayWords()

			if todayWords.exists():
				
				try:
					# 오늘 자 단어들 중에서 현재 선택된 단어와 같은 단어가 있으면 
					# 그걸 수정해서 빈도수를 더해준다.
					word = get_object_or_404(todayWords, value=key)
					word.freq += value
					word.news.add(n)
					word.save()
					print word.value+"("+str(word.freq)+")"

				except Exception, e:
					# 같은 단어가 디비에 없으면 단어 생성
					Words.objects.create(
						value=key,
						freq=value,
						date=datetime.now().strftime('%Y-%m-%d'),
					).news.add(n)
				
			else:
				Words.objects.create(
					value=key,
					freq=value,
					date=datetime.now().strftime('%Y-%m-%d'),
				).news.add(n)
			

# data폴더 내의 문서들을 전부 읽어들여
# 각 문서 내 단어들의 빈도수를 측정한 딕셔너리들을

# 각 문서의 단어 빈도수 딕셔너리를 전체 딕셔너리에 합산한다.
def addup(dict):
	result={}
	for key in dict:
		if not key in result.keys():
			result[key]=dict[key]
		else:
			result[key]+=dict[key]

	return OrderedDict(sorted(result.items(), key=itemgetter(1), reverse=True))


def print_dict(dict):
	result=""
	for k,v in dict.items():
		data = k+"("+str(v)+")"+" "
		result += data 
	print result+"\n" 