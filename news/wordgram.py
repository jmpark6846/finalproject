# -*- coding: utf-8 -*-
from konlpy.tag import Hannanum
from operator import itemgetter
from konlpy.utils import pprint
from collections import OrderedDict
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
def hannanum_analyze_22(content):
	# content = remove_puc_marks(content) #문장 부호 제거
	dictionary={}
	h= Hannanum()
	tags={
		'NC':'보통명사',
		'NQ':'고유명사',
		# 'NB':'의존명사',	
		# 'NN':'수사' ,
		# 'NP':'대명사' , 
		# 'PV':'동사', 
		# 'PA':'형용사',
		# 'PX':'보조 용언',
		# 'MM':'관형사' , 
		# 'MA':'부사',
	}	

	# 내용으로 품사 분석해서 딕셔너리로 반환
	words = h.pos(content,22)
	
	for t in words:
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

	# dictionary=remove_stopwords(dictionary)	# 불용어 제거
	dictionary=OrderedDict(sorted(dictionary.items(), key=itemgetter(1), reverse=True))
	
	return dictionary

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