# -*- coding: utf-8 -*-
from operator import itemgetter
from collections import OrderedDict
import os
import math
from os import listdir

# 문서의 단어 dictionary가 주어졌을때 단어 word에 대한 IDF값을 구한다.
def idf_value(dict_map, word):
	word_count=0

	for dict_elem in dict_map:
		if word in dict_elem.keys():
			word_count+=1

	if word_count is 0:
		word_count=1

	return math.log(len(dict_map)/word_count)

# 문서의 단어 dictionary가 주어졌을때 문서내 단어들의 IDF값을 구한다.
def idf_analyze(dict_map, dictionary):
	idf_dict = OrderedDict()
	
	for word in dictionary:
		idf_dict[word]=idf_value(dict_map, word)

	idf_dict = OrderedDict(sorted(idf_dict.items(), key=itemgetter(1), reverse=True))
	return idf_dict

# 한 문서의 tf_idf값을 dictionary로 반환한다.
def tf_idf_analyze(dict_map, dictionary):
	dict_tf = dictionary
	dict_idf = idf_analyze(dict_map, dictionary)

	tf_idf_dict = OrderedDict()
	for word in dict_tf.keys():
		tf_idf_dict[word] = dict_tf[word] * dict_idf[word]

	tf_idf_dict = OrderedDict(sorted(tf_idf_dict.items(), key=itemgetter(1), reverse=True))

	return tf_idf_dict

def tf_idf_map(dict_map):
	tf_idf_dic={}
	for news, dic in dict_map.items():
		tf_idf_dic[news]=tf_idf_analyze(dict_map.values(), dic)
	return tf_idf_dic



