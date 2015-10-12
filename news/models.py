# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime

NEWS_TYPE = (
    ('politics', '정치'),
    ('society', '사회'),
)
TAGS=(
        ('NC','보통명사'),
        ('NQ','고유명사'),
)


class Company(models.Model):
    name = models.CharField(max_length=256, blank=True, default="")
    tend = models.CharField(max_length=256, default="")

    def __unicode__(self):
        return self.name

    def get_today_news(self):
        now = datetime.now().strftime('%Y-%m-%d')
        return self.news.filter(date=now)



class News(models.Model):
    user = models.ForeignKey('auth.User', related_name='news')
    date = models.DateTimeField()
    title = models.CharField(max_length=256, blank=True, default="")
    content = models.TextField()
    link = models.CharField(max_length=256, blank=True, default="")
    type = models.CharField(choices=NEWS_TYPE, default="society", max_length=100)
    company = models.ForeignKey('Company', related_name='news')

    class Meta:
        ordering = ('date',)

    def getLikesCount(self):
        return NewsLikes.objects.filter(news=self).count()

    def getDislikesCount(self):
        return NewsDislikes.objects.filter(news=self).count()

    likes = property(getLikesCount)
    dislikes = property(getDislikesCount)

    def __unicode__(self):
        return self.title

class NewsLikes(models.Model):
    news = models.ForeignKey(News)
    user = models.ForeignKey('auth.User')

class NewsDislikes(models.Model):
    news = models.ForeignKey(News)
    user = models.ForeignKey('auth.User')

def getTodayNews():
    now = datetime.now().strftime('%Y-%m-%d')
    return News.objects.filter(date=now)


