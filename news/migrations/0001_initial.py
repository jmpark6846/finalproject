# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=256, blank=True)),
                ('tend', models.CharField(default=b'', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('title', models.CharField(default=b'', max_length=256, blank=True)),
                ('content', models.TextField()),
                ('link', models.CharField(default=b'', max_length=256, blank=True)),
                ('type', models.CharField(default=b'society', max_length=100, choices=[(b'politics', b'\xec\xa0\x95\xec\xb9\x98'), (b'society', b'\xec\x82\xac\xed\x9a\x8c')])),
                ('company', models.ForeignKey(related_name='news', to='news.Company')),
                ('user', models.ForeignKey(related_name='news', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date',),
            },
        ),
        migrations.CreateModel(
            name='Words',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=50)),
                ('freq', models.IntegerField(default=0)),
                ('tag', models.CharField(default=b'NC', max_length=100, choices=[(b'NC', b'\xeb\xb3\xb4\xed\x86\xb5\xeb\xaa\x85\xec\x82\xac'), (b'NQ', b'\xea\xb3\xa0\xec\x9c\xa0\xeb\xaa\x85\xec\x82\xac')])),
                ('date', models.DateTimeField()),
                ('rank', models.IntegerField(default=0)),
                ('news', models.ManyToManyField(related_name='words', to='news.News')),
            ],
        ),
    ]
