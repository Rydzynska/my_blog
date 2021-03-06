# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-16 12:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_auto_20160516_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(error_messages={'blank': 'Please enter your e-mail', 'invalid': 'Please enter your e-mail', 'null': 'Please enter your e-mail'}, max_length=254, verbose_name='Your e-mail address'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(error_messages={'blank': 'Please enter your name', 'null': 'Please enter your name'}, max_length=100, verbose_name='Your name'),
        ),
    ]
