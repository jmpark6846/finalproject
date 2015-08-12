# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(default=b'', max_length=256, blank=True)),
                ('content', models.TextField()),
                ('link', models.CharField(default=b'', max_length=256, blank=True)),
                ('type', models.CharField(default=b'\xec\xa0\x95\xec\xb9\x98', max_length=100, choices=[(b'politics', b'\xec\xa0\x95\xec\xb9\x98'), (b'society', b'\xec\x82\xac\xed\x9a\x8c')])),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
    ]
