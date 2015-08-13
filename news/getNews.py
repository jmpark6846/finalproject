# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import wordgram
import urllib2
import sys
from models import News
if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding("utf-8")

# "http://www.ytn.co.kr/news/news_list_0101.html"
def getNews(user, url):
	htmltext = urllib2.urlopen(url).read()
	soup = BeautifulSoup(htmltext, from_encoding="utf-8")

	newsList = soup.findAll('dl',attrs={"class","news_list_v2014"})
	newsLink = []
	news_db = []

	# 뉴스 목록에서 각각 뉴스의 url을 긁어옵니다.
	for news in newsList:
		newsLink.append('http://www.ytn.co.kr'+news.find('a')['href'])

	# 긁어온 각 뉴스 url을 열어서 뉴스 제목, 내용을 긁어와 뉴스 객체를 만듭니다.
	for link in newsLink :
		news_dict ={}
		htmltext = urllib2.urlopen(link).read()
		soup = BeautifulSoup(htmltext, from_encoding="utf-8")
		title = soup.find('div', attrs={"class","article_tit"}).get_text()
		content = soup.find('div',attrs={"class","article_paragraph"}).get_text()

		News.objects.create(
			title=title,
			content=content,
			link=link,
			type='society',
			user=user,
		)
		
	# content_dict.append(wordgram.wordgram_analyze_string(content))
	# print menu[int(i)]+"\n"
	# result = wordgram.addup(content_dict)
	# wordgram.print_dict(result)
	# print result