# -*- coding: utf-8 -*-
from django.db import models
from news.models import News
from datetime import datetime


NEWS_TYPE = (
    ('politics', '정치'),
    ('society', '사회'),
)
TAGS=(
    ('NC','보통명사'),
    ('NQ','고유명사'),
)



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

def getWordsAt(date):
    words = Words.objects.filter(date=date.strftime('%Y-%m-%d')).order_by("-freq");
    return words
