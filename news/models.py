# -*- coding: utf-8 -*-
from django.db import models

NEWS_TYPE = (
	('politics', '정치'),
	('society', '사회'),
)

class News(models.Model):
	user = models.ForeignKey('auth.User', related_name='news')
	created_at = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=256, blank=True, default="")
	content = models.TextField()
	link = models.CharField(max_length=256, blank=True, default="")
	type = models.CharField(choices=NEWS_TYPE, default="정치", max_length=100)

	class Meta:
		ordering = ('created_at',)
