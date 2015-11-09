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


