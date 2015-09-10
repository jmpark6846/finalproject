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

    def __unicode__(self):
        return self.title


def getTodayNews():
    now = datetime.now().strftime('%Y-%m-%d')
    return News.objects.filter(date=now)


class Words(models.Model):
    value = models.CharField(max_length=50)
    freq = models.IntegerField(default=0)
    tag = models.CharField(choices=TAGS, default="NC", max_length=100)
    news = models.ManyToManyField(News, related_name="words")
    date = models.DateTimeField()
    rank = models.IntegerField(default=0)

    def __unicode__(self):
        return self.value


def getTodayWords():
    now = datetime.now().strftime('%Y-%m-%d')
    return Words.objects.filter(date=now)
