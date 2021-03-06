# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 08:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20170523_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailorder',
            name='delivered_to_post_office',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mailorder',
            name='payment_received',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mailorder',
            name='printed',
            field=models.BooleanField(default=False),
        ),
    ]
