# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-18 01:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0012_auto_20180217_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated Time'),
        ),
    ]
