# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 18:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20170604_0842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailorder',
            name='pdf_letter',
        ),
        migrations.AddField(
            model_name='mailorder',
            name='pdf_letter_url',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
