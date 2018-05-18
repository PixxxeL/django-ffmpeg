# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-30 05:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_ffmpeg', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='thumb_frame',
            field=models.PositiveIntegerField(default=0, verbose_name='Frame number for thumbnail'),
        ),
    ]