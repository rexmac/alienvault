# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-12 03:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0002_auto_20180211_0453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='alien_vault_id',
            field=models.CharField(default=b'4uGJTybowFmT', max_length=12),
        ),
    ]
