# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-19 21:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('popular_proposal', '0011_auto_20160418_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposaltemporarydata',
            name='rejected_reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]
