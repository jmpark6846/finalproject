# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime

NEWS_TYPE = (
	('politics', '정치'),
	('society', '사회'),
)
TAGS={
		'NC':'보통명사',
		'NQ':'고유명사',
		# 'NB':'의존명사',	
		# 'NN':'수사' ,
		# 'NP':'대명사' , 
		# 'PV':'동사', 
		# 'PA':'형용사',
		# 'PX':'보조 용언',
		# 'MM':'관형사' , 
		# 'MA':'부사',
}	

class News(models.Model):
	user = models.ForeignKey('auth.User', related_name='news')
	date = models.DateTimeField()
	title = models.CharField(max_length=256, blank=True, default="")
	content = models.TextField()
	link = models.CharField(max_length=256, blank=True, default="")
	type = models.CharField(choices=NEWS_TYPE, default="society", max_length=100)

	class Meta:
		ordering = ('date',)

	def __unicode__(self):
		return self.title

class Words(models.Model):
	value = models.CharField(max_length=50)
	freq = models.IntegerField(default=0)
	tag = models.CharField(choices=TAGS, default="NC")
	news = models.ForeignKey(News, related_name="words")

	def __unicode__(self):
		return self.value