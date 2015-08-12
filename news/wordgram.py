# # -*- coding: utf-8 -*-
# from konlpy.tag import Hannanum
# from operator import itemgetter
# from konlpy.utils import pprint
# from collections import OrderedDict
# import os
# import fileio
# from os import listdir

# # 문장부호제거
# def remove_puc_marks(contents):
# 	pmarks=['·','?', '\/', '(', ')', ',', '.', ':', '{', '}', ';', '!', '@', '#', '$', '%', '^', '&', '-', '_', '=', '<', '>', '*']
# 	for mark in pmarks:
# 		contents= contents.replace(mark,' ')
# 	return contents

# # 불용어 제거
# def remove_stopwords(dictionary):
# 	file = open("stopwords/stopwords_kr.txt","r")
# 	stopwords = file.readlines()

# 	for stopword in stopwords:
# 		sw = stopword.replace('\n','')
# 		if sw in dictionary:
# 			del dictionary[sw]

# 	return dictionary

# # 한나눔 9품사 분류
# def hannanum_analyze(content):
# 	dictionary={}
# 	h= Hannanum()
# 	words = h.pos(content)
# 	for tuple in words:
# 		value = tuple[1]
# 		if value == "N" or value == "P" or value == "M":
# 			key = tuple[0]
# 			# '먹' 같은 용언에는 '-다'를 붙여 '먹다' 같은 동사로 키값 사용
# 			if value == "P":
# 				key += u"다"

# 			if not key in dictionary.keys():
# 				dictionary[key] =1
# 			else :
# 				dictionary[key] +=1
# 	return OrderedDict(sorted(dictionary.items(), key=itemgetter(1), reverse=True))

# # 한나눔 22품사 분류
# def hannanum_analyze_22(content):
# 	dictionary={}
# 	h= Hannanum()
# 	tags={
# 		'NC':'보통명사',
# 		'NQ':'고유명사',
# 		# 'NB':'의존명사',	
# 		# 'NN':'수사' ,
# 		# 'NP':'대명사' , 
# 		# 'PV':'동사', 
# 		# 'PA':'형용사',
# 		# 'PX':'보조 용언',
# 		# 'MM':'관형사' , 
# 		# 'MA':'부사',
# 	}	
# 	words = h.pos(content,22)
	
# 	for t in words:
# 		key = t[0]
# 		value = t[1]
		
# 		if value in tags.keys():
# 			# '먹' 같은 용언에는 '-다'를 붙여 '먹다' 같은 동사로 키값 사용
# 			if value.startswith("P"):
# 				key += u"다"
# 			key= key# + "		["+tags[value]+"]"

# 			if not key in dictionary.keys():
# 				dictionary[key] =1
# 			else :
# 				dictionary[key] +=1
# 			# print key + " " + value

# 	dictionary=remove_stopwords(dictionary)	# 불용어 제거
# 	dictionary=OrderedDict(sorted(dictionary.items(), key=itemgetter(1), reverse=True))
	
# 	return dictionary

# # 한나눔 22품사 분류, 단어에 품사표시
# def hannanum_analyze_22_key(content):
# 	dictionary={}
# 	h= Hannanum()
# 	tags={
# 		'NC':'보통명사',
# 		'NQ':'고유명사',
# 		# 'NB':'의존명사',	
# 		# 'NN':'수사' ,
# 		# 'NP':'대명사' , 
# 		# 'PV':'동사', 
# 		# 'PA':'형용사',
# 		# 'PX':'보조 용언',
# 		# 'MM':'관형사' , 
# 		# 'MA':'부사',
# 	}	
# 	words = h.pos(content,22)
	
# 	for t in words:
# 		key = t[0]
# 		value = t[1]
		
# 		if value in tags.keys():
# 			# '먹' 같은 용언에는 '-다'를 붙여 '먹다' 같은 동사로 키값 사용
# 			if value.startswith("P"):
# 				key += u"다"
# 			key= key+ "["+value+"]"

# 			if not key in dictionary.keys():
# 				dictionary[key] =1
# 			else :
# 				dictionary[key] +=1
# 			# print key + " " + value

# 	dictionary=remove_stopwords(dictionary)	# 불용어 제거
# 	dictionary=OrderedDict(sorted(dictionary.items(), key=itemgetter(1), reverse=True))
	
# 	return dictionary

# # data폴더 내의 문서들을 전부 읽어들여
# # 각 문서 내 단어들의 빈도수를 측정한 딕셔너리들을
# # dict_map리스트에 저장 후 리턴
# def wordgram_analyze(dirpath):
# 	dict_map=[]
# 	file_list=listdir(dirpath)
# 	for file in file_list:
# 		extension = os.path.splitext(file)[1]
# 		if extension !='.txt':
# 			continue
# 		file = dirpath + file
# 		file_contents = fileio.read_file(file)			#파일의 내용을 읽어온다.
# 		file_contents= remove_puc_marks(file_contents)	#문장 부호제거
# 		file_dict = hannanum_analyze_22(file_contents)	#형태소별로 딕셔너리에 분류
# 		# file_dict = hannanum_analyze_22_key(file_contents)	#형태소별로 딕셔너리에 분류
# 		dict_map.append(file_dict)						#전체 딕셔너리에 추가한다.
# 	return dict_map

# def wordgram_analyze_string(content):
# 	file_contents= remove_puc_marks(content)	#문장 부호제거
# 	file_dict = hannanum_analyze_22(file_contents)	#형태소별로 딕셔너리에 분류
# 	return file_dict

# def print_dict(dict):
# 	result=""
# 	for k,v in dict.items():
# 		data = str(k)+"("+str(v)+")"+" "
# 		result += data 
# 	print result+"\n" 

# # 각 문서의 단어 빈도수 딕셔너리를 전체 딕셔너리에 합산한다.
# def addup(list):
# 	result={}
# 	for dict in list:
# 		for key in dict:
# 			if not key in result.keys():
# 				result[key]=dict[key]
# 			else:
# 				result[key]+=dict[key]
	
# 	return OrderedDict(sorted(result.items(), key=itemgetter(1), reverse=True))