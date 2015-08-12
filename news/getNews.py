# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import wordgram
import urllib2
import sys
if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding("utf-8")

# "http://www.ytn.co.kr/news/news_list_0101.html"
def getNews(url):
	htmltext = urllib2.urlopen(url).read()
	soup = BeautifulSoup(htmltext, from_encoding="utf-8")

	newsList = soup.findAll('dl',attrs={"class","news_list_v2014"})
	newsLink = []
	news_db = []

	for news in newsList:
		newsLink.append('http://www.ytn.co.kr'+news.find('a')['href'])

	for link in newsLink :
		news_dict ={}
		htmltext = urllib2.urlopen(link).read()
		soup = BeautifulSoup(htmltext, from_encoding="utf-8")
		title = soup.find('div', attrs={"class","article_tit"}).get_text()
		content = soup.find('div',attrs={"class","article_paragraph"}).get_text()
		news_dict ={
			'title':title,
			'content':content,
			'link':link,
			'type':'society',
		}
		
		news_db.append(news_dict)

	return news_db

	# content_dict.append(wordgram.wordgram_analyze_string(content))
	# print menu[int(i)]+"\n"
	# result = wordgram.addup(content_dict)
	# wordgram.print_dict(result)
	# print result