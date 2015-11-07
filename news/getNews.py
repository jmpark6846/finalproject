# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import wordgram
import urllib2
import sys
from models import News, Company
from datetime import datetime

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding("utf-8")


##### 한국일보  ###
def crawlNews_hankook(user):
	NEWS_TYPE = {
		'1': 'politics',
		'3': 'society',
	}
	company = Company.objects.get(name="한국일보")
	for i in NEWS_TYPE.keys() :
		url = "http://www.hankookilbo.com/l.aspx?c=" + i

		# html source
		htmltext = urllib2.urlopen(url).read()
		soup = BeautifulSoup(htmltext, from_encoding="utf-8")

		# 기사 읽기
		article_list = soup.find('ul',attrs={'class','article-list-1'})

		newsList = article_list.findAll('div',attrs={"class","title"})
		newsLink = []
		for news in newsList:
			newsLink.append("http://www.hankookilbo.com" + news.find('a')['href'])

		for link in newsLink :
			htmltext = urllib2.urlopen(link).read()
			soup = BeautifulSoup(htmltext, from_encoding="utf-8")
			try:
				content_div = soup.find('div', attrs={"class",'content-2'})
				title = content_div.find('h3').get_text()
				content = content_div.find('div', {"id":"article-body"}).get_text()
			except AttributeError:
				print company.name+' AttributeError : ' + link

			if len(content) <= 100:
				continue
			else:
				News.objects.create(
					title=title,
					content=content,
					link=link,
					type=NEWS_TYPE[i],
					user=user,
					date=datetime.now().strftime('%Y-%m-%d'),
					company=company,
				)


##### 서울신문  ###
def crawlNews_seoul(user):
	NEWS_TYPE = {
		'politics': 'politics',
		'society': 'society',
	}
	company = Company.objects.get(name="서울신문")
	for i in NEWS_TYPE.keys() :
		url = "http://www.seoul.co.kr/news/newsList.php?section=" + i

		# html source
		htmltext = urllib2.urlopen(url).read()
		soup = BeautifulSoup(htmltext, from_encoding="utf-8")

		# 기사 읽기

		newsList = soup.findAll('dl',attrs={"class","article"})
		newsLink = []
		print len(newsList)
		for news in newsList:
			newsLink.append("http://www.seoul.co.kr" + news.find('span').find('a')['href'])

		for link in newsLink :
			htmltext = urllib2.urlopen(link).read()
			soup = BeautifulSoup(htmltext, from_encoding="utf-8")
			try:
				title_div = soup.find('div',attrs={"class", "atic_title"})
				if title_div is None:
					title = soup.find('div', attrs={"class", "a_title"})
				else:
					title = title_div.find('h3').get_text()

				html = soup.find('div',attrs={"class", "atic_txt1"})
				if html is None:
					html = soup.find('div', {"id": "CmAdContent"})
				else:
					html = html
				content = html.get_text()

			except AttributeError:
				print company.name+' AttributeError : ' + link

			if len(content) <= 100:
				continue
			else:
				News.objects.create(
					title=title,
					content=content,
					html= html,
					link=link,
					type=NEWS_TYPE[i],
					user=user,
					date=datetime.now().strftime('%Y-%m-%d'),
					company=company,
				)


##### 동아일보  ###
def crawlNews_donga(user):
	NEWS_TYPE = {
		'Politics': 'politics',
		'Society': 'society',
	}
	company = Company.objects.get(name="동아일보")
	for i in NEWS_TYPE.keys() :
		url = "http://news.donga.com/"+i

		# html source
		htmltext = urllib2.urlopen(url).read()

		soup = BeautifulSoup(htmltext, 'html.parser')

		# 기사 읽기
		newsList = soup.findAll('div',attrs={"class","articleList"})
		newsLink = []
		for news in newsList:
			newsLink.append(news.find('a')['href'])

		for link in newsLink :
			htmltext = urllib2.urlopen(link).read()
			try:
				soup = BeautifulSoup(htmltext.decode('utf-8'), 'html.parser')

				title_div = soup.find('div',attrs={"class","article_title02"})
				title = title_div.find('h1').get_text()

				html = soup.find('div',attrs={"class","article_txt"})
				content = html.get_text()
				script = content.find('function')
				content = content[:script]

			except AttributeError:
				print company.name+' AttributeError : ' + link

			if len(content) <= 100:
				continue
			else:
				News.objects.create(
					title=title,
					content=content,
					html=html,
					link=link,
					type=NEWS_TYPE[i],
					user=user,
					date=datetime.now().strftime('%Y-%m-%d'),
					company=company,
				)


######## 국민일보
def crawlNews_km(user):
	NEWS_TYPE = {
		'pol': 'politics',
		'soc': 'society',
	}
	company = Company.objects.get(name="국민일보")
	for i in NEWS_TYPE.keys() :
		url = "http://news.kmib.co.kr/article/list.asp?sid1="+i

		# html source
		htmltext = urllib2.urlopen(url).read()

		soup = BeautifulSoup(htmltext, from_encoding="utf-8")

		# 기사 읽기
		newsList = soup.findAll('dl',attrs={"class","nws"})
		newsLink = []
		for news in newsList:
			newsLink.append("http://news.kmib.co.kr/article/"+news.find('a')['href'])

		for link in newsLink :
			htmltext = urllib2.urlopen(link).read()
			try:
				soup = BeautifulSoup(htmltext, 'html.parser')
				title_div = soup.find('div',attrs={"class","nwsti"})
				title = title_div.find('h2').get_text()
				html = soup.find('div',attrs={"class","tx"})
				content = html.get_text()
			except AttributeError:
				print company.name+' AttributeError : ' + link

			if len(content) <= 100:
				continue
			else:
				News.objects.create(
					title=title,
					content=content,
					html=html,
					link=link,
					type=NEWS_TYPE[i],
					user=user,
					date=datetime.now().strftime('%Y-%m-%d'),
					company=company,
				)


def crawlNews_hani(user):
	NEWS_TYPE = {
		'politics': 'politics',
		'society': 'society',
	}
	company = Company.objects.get(name="한겨례")
	for i in NEWS_TYPE.keys():
		url = "http://www.hani.co.kr/arti/" + i
		htmltext = urllib2.urlopen(url).read()
		soup = BeautifulSoup(htmltext, from_encoding="utf-8")

		soup = soup.find('div',attrs={"class","section-list-area"})
		newsList = soup.findAll('h4')
		newsLink = []
		for news in newsList:
			newsLink.append("http://www.hani.co.kr"+news.find('a')['href'])

		for link in newsLink :
			htmltext = urllib2.urlopen(link).read()
			try:
				soup = BeautifulSoup(htmltext, from_encoding="utf-8")
				title_div = soup.find('div',attrs={"class","article-head"})
				title = title_div.find('span',attrs={"class","title"}).get_text()
				html = soup.find('div',attrs={"class","text"})
				content = html.get_text()
			except AttributeError:
				print company.name+' AttributeError : ' + link

			if len(content) <= 100:
				continue
			else:
				News.objects.create(
					title=title,
					content=content,
					html=html,
					link=link,
					type=NEWS_TYPE[i],
					user=user,
					date=datetime.now().strftime('%Y-%m-%d'),
					company=company,
				)


def crawlNews_pressian(user):
	NEWS_TYPE = {
		6: 'politics',
		8: 'society',
	}
	company = Company.objects.get(name="프레시안")
	for i in NEWS_TYPE.keys():
		url = "http://www.pressian.com/news/section_list_all.html?sec_no=6" + str(i)
		htmltext = urllib2.urlopen(url).read()
		soup = BeautifulSoup(htmltext, from_encoding="utf-8")

		newsList = soup.findAll('div',attrs={"class","list_tt"})
		newsLink = []
		for news in newsList:
			newsLink.append(news.find('a')['href'])

		for link in newsLink :
			htmltext = urllib2.urlopen(link).read()
			try:
				soup = BeautifulSoup(htmltext, from_encoding="utf-8")
				title_div = soup.find('div',attrs={"class","hbox"})
				title = title_div.find('div',attrs={"class","hboxtitle"}).get_text()
				html = soup.find('div',attrs={"class","smartOutput"})
				content = html.get_text()
			except AttributeError:
				print company.name+' AttributeError : ' + link

			if len(content) <= 100:
				continue
			else:
				News.objects.create(
					title=title,
					content=content,
					html=html,
					link=link,
					type=NEWS_TYPE[i],
					user=user,
					date=datetime.now().strftime('%Y-%m-%d'),
					company=company,
				)


# "http://www.ytn.co.kr/news/news_list_0101.html"
def crawlNews_ytn(user):
	NEWS_TYPE = {
		'1': 'politics',
		'3': 'society',
	}
	company = Company.objects.get(name="YTN")
	for i in NEWS_TYPE.keys():
		url = 'http://www.ytn.co.kr/news/news_list_010'+i+'.html'
		htmltext = urllib2.urlopen(url).read()
		soup = BeautifulSoup(htmltext, from_encoding="utf-8")

		newsList = soup.findAll('dl',attrs={"class","news_list_v2014"})
		newsLink = []

		# 뉴스 목록에서 각각 뉴스의 url을 긁어옵니다.
		for news in newsList:
			newsLink.append('http://www.ytn.co.kr'+news.find('a')['href'])

		# 긁어온 각 뉴스 url을 열어서 뉴스 제목, 내용을 긁어와 뉴스 객체를 만듭니다.
		for link in newsLink :
			htmltext = urllib2.urlopen(link).read()
			try:
				soup = BeautifulSoup(htmltext, from_encoding="utf-8")
				title = soup.find('div', attrs={"class","article_tit"}).get_text()
				html = soup.find('div',attrs={"class","article_paragraph"})
				content = html.get_text()
			except AttributeError:
				print company.name+' AttributeError : ' + link

			if len(content) <= 100:
				continue
			else:
				News.objects.create(
					title=title,
					content=content,
					html=html,
					link=link,
					type=NEWS_TYPE[i],
					user=user,
					date=datetime.now().strftime('%Y-%m-%d'),
					company=company,
				)


def crawlNews_joongang(user):
	NEWS_TYPE = ["politics","society"]
	company = Company.objects.get(name="중앙일보")
	url = ['http://article.joins.com/news/list/list.asp?ctg=10&sc=JO&dt=','http://article.joins.com/news/list/list_society_code.asp?society=society&sc=JO&dt=']

	for i in range(0,len(NEWS_TYPE)) :

		# html source 5
		htmltext = urllib2.urlopen(url[i]).read()

		soup = BeautifulSoup(htmltext, from_encoding="utf-8")

		# 기사 읽기
		soup = soup.find('div',attrs={"class","bd"})
		newsList = soup.findAll('li')
		newsLink = []
		for news in newsList:
			newsLink.append(news.find('a')['href'])

		for link in newsLink :
			htmltext = urllib2.urlopen(link).read()
			soup = BeautifulSoup(htmltext, from_encoding="utf-8")
			try:
				title = soup.find('h1',attrs={"class","headline"}).get_text()
				html = soup.find('div', attrs={"class","article_body"})
				content=html.get_text()
			except AttributeError:
				print company.name+' AttributeError : ' + link
				continue

			if len(content) <= 100:
				continue
			else:
				News.objects.create(
					title=title,
					content=content,
					html=html,
					link=link,
					type=NEWS_TYPE[i],
					user=user,
					date=datetime.now().strftime('%Y-%m-%d'),
					company=company,
				)

def crawlNews_ohmynews(user):
	NEWS_TYPE = {
		'400':"politics",
		'200':"society",
	}

	company = Company.objects.get(name="오마이뉴스")
	for i in NEWS_TYPE.keys() :
		url = "http://www.ohmynews.com/NWS_Web/ArticlePage/Total_Article.aspx?PAGE_CD=C0"+i

		# html source
		htmltext = urllib2.urlopen(url).read()
		soup = BeautifulSoup(htmltext, from_encoding="utf-8")

		# 기사 읽기
		newsList = soup.findAll('div',attrs={"class","news_list"})
		newsLink = []

		for news in newsList:
			newsLink.append('http://www.ohmynews.com'+news.find('a')['href'])

		for link in newsLink :
			htmltext = urllib2.urlopen(link).read()
			soup = BeautifulSoup(htmltext, from_encoding="utf-8")
			try:
				title = soup.find('h3',attrs={"class","tit_subject"})
				if title == None:
					title = soup.find('h5',attrs={"class","tit_subject"})

					if title == None:
						continue

				title = title.get_text()
				html = soup.find('div',attrs={"class","at_contents"})
				content = html.get_text()
			except AttributeError:
				print company.name+' AttributeError : ' + link
				continue

			if len(content) <= 100:
				continue
			else:
				News.objects.create(
					title=title,
					content=content,
					html=html,
					link=link,
					type=NEWS_TYPE[i],
					user=user,
					date=datetime.now().strftime('%Y-%m-%d'),
					company=company,
				)

def crawlNews_chosun(user):
	NEWS_TYPE = {
		'2':"politics",
		'3':"society",
	}
	company = Company.objects.get(name="조선일보")
	for i in NEWS_TYPE.keys() :
		url = "http://news.chosun.com/svc/list_in/list_title.html?catid="+i
		htmltext = urllib2.urlopen(url).read()
		soup = BeautifulSoup(htmltext, from_encoding="utf-8")

		newsList = soup.findAll('dl',attrs={"class","list_item"})
		newsLink = []

		for news in newsList:
			
			newsLink.append(news.find('a')['href'])

		for link in newsLink : 
			htmltext = urllib2.urlopen(link).read()
			soup = BeautifulSoup(htmltext, from_encoding="utf-8")
			# title
			try:
				title_div = soup.find('div',attrs={"class","news_title_text"})
				title = title_div.find('h1').get_text()
				contents = soup.findAll('div', attrs={"class", "par"})
				html=""
				content=""
				for item in contents:
					html+=str(item)
					content += item.get_text()
			except AttributeError:
				print company.name+' AttributeError : ' + link
				continue

			if len(content) <= 100:
				continue
			else:
				News.objects.create(
					title=title,
					content=content,
					html=html,
					link=link,
					type=NEWS_TYPE[i],
					user=user,
					date=datetime.now().strftime('%Y-%m-%d'),
					company=company,
				)



