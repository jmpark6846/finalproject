# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_news_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ('date',)},
        ),
        migrations.RemoveField(
            model_name='news',
            name='created_at',
        ),
        migrations.AddField(
            model_name='news',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 13, 18, 3, 2, 782000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
