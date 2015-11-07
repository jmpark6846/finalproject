# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0007_auto_20151020_1130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsdislikes',
            name='news',
        ),
        migrations.RemoveField(
            model_name='newsdislikes',
            name='user',
        ),
        migrations.RemoveField(
            model_name='newslikes',
            name='news',
        ),
        migrations.RemoveField(
            model_name='newslikes',
            name='user',
        ),
        migrations.AddField(
            model_name='news',
            name='dislikes',
            field=models.ManyToManyField(related_name='disliked_news', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='news',
            name='likes',
            field=models.ManyToManyField(related_name='liked_news', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='NewsDislikes',
        ),
        migrations.DeleteModel(
            name='NewsLikes',
        ),
    ]
