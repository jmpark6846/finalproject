# -*- coding: utf-8 -*-

from konlpy.tag import Hannanum
from collections import Counter
from models import *
from word.models import Words
from tfidf import tf_idf_map

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
		news.id : 분석 결과 dictionary,
		news.id : 분석 결과 dictionary,
		...
	}
	"""
	pos_dics = {}
	news = getTodayNews()
	
	for n in news :
		content = remove_puc_marks(n.content) # 문장 부호 제거
		words_dic = h.pos(content,22)			# 형태소 제거
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

	print "tf-idf"
	analyzed_dics=tf_idf_map(pos_dics) 			# tfidf 계산

	return analyzed_dics


def create_words(analyzed_dics):
	dic = {}
	"""
	dic=
	{
		단어 : [뉴스,뉴스,],
	}
	"""
	for news,data in analyzed_dics.items():
		sorted_data = Counter(data).most_common(50)

		for item in sorted_data:
			keyword=item[0]
			if keyword not in dic:
				dic[keyword]=[news]
			else:
				dic[keyword].append(news)

	for keyword, news_list in dic.items():
		if len(news_list) <= 3:
			continue
		elif len(keyword) > 1:
			word = Words.objects.create(
				value=keyword,
				freq=len(news_list),
				date=datetime.now().strftime('%Y-%m-%d'),
			)
			for n in news_list:
				word.news.add(n)
