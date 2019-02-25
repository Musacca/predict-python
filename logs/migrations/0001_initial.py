# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-25 10:14
from __future__ import unicode_literals

import django.db.models.deletion
import jsonfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('path', models.CharField(max_length=200)),
                ('properties', jsonfield.fields.JSONField(default={})),
            ],
        ),
        migrations.CreateModel(
            name='Split',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config', jsonfield.fields.JSONField(default={})),
                ('type', models.CharField(choices=[('single', 'Single'), ('double', 'Double')], default='single',
                                          max_length=20)),
                ('original_log',
                 models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                   related_name='original_log', to='logs.Log')),
                ('test_log', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                               related_name='test_log', to='logs.Log')),
                ('training_log', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                                   related_name='training_log', to='logs.Log')),
            ],
        ),
    ]
