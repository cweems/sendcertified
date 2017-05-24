# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 08:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20170523_0755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailorder',
            name='recipient_state',
        ),
        migrations.RemoveField(
            model_name='mailorder',
            name='sender_state',
        ),
        migrations.AlterField(
            model_name='mailorder',
            name='recipient_unit',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='mailorder',
            name='sender_unit',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]