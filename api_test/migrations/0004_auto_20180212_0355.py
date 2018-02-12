# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-12 03:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0003_auto_20180212_0345'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alien_vault_id', models.CharField(default=b'ZXK7Z4hGLZNL', max_length=12)),
            ],
        ),
        migrations.RenameModel(
            old_name='Visits',
            new_name='Visit',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
        migrations.AlterField(
            model_name='visit',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='api_test.User'),
        ),
    ]