# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-11 18:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('preguntales', '0003_outboundmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.FileField(upload_to=b'attachments/%Y/%m/%d')),
                ('name', models.CharField(max_length=255)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='preguntales.Answer')),
            ],
        ),
    ]
