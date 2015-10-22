# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_newsdislikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsdislikes',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 20, 2, 30, 2, 445000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='newslikes',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 20, 2, 30, 9, 385000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
