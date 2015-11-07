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
    html = models.TextField()
    content = models.TextField()
    link = models.CharField(max_length=256, blank=True, default="")
    type = models.CharField(choices=NEWS_TYPE, default="society", max_length=100)
    company = models.ForeignKey('Company', related_name='news')

    likes    = models.ManyToManyField('auth.User', related_name = "liked_news")
    dislikes = models.ManyToManyField('auth.User', related_name = "disliked_news")

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('date',)


def getTodayNews():
    now = datetime.now().strftime('%Y-%m-%d')
    return News.objects.filter(date=now)




