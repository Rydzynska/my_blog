# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-18 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20160415_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
