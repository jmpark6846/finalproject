# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_auto_20151103_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='html',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
