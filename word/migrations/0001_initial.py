# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20151002_1143'),
    ]

    operations = [
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
