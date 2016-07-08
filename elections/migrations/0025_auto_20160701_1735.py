# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-01 17:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0024_auto_20160307_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='elections',
            field=models.ManyToManyField(default=None, related_name='candidates', to='elections.Election'),
        ),
        migrations.AlterField(
            model_name='election',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='elections', to='popolo.Area'),
        ),
    ]