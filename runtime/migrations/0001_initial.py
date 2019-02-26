# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-26 15:38
from __future__ import unicode_literals

import django.db.models.deletion
import jsonfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('logs', '0001_initial'),
        ('pred_models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DemoReplayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('running', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='XEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config', models.CharField(default='', max_length=500, null=True)),
                ('xid', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='XLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config', models.CharField(default='', max_length=500, null=True)),
                ('real_log', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='real_log',
                                               to='logs.Log')),
            ],
        ),
        migrations.CreateModel(
            name='XTrace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config', models.CharField(default='', max_length=500, null=True)),
                ('name', models.CharField(default='', max_length=30, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('first_event', models.DateTimeField(null=True)),
                ('last_event', models.DateTimeField(null=True)),
                ('n_events', models.IntegerField(default=0)),
                ('error', models.CharField(default='', max_length=500, null=True)),
                ('real_log', models.IntegerField()),
                ('reg_results', jsonfield.fields.JSONField(default={})),
                ('class_results', jsonfield.fields.JSONField(default={})),
                ('reg_actual', jsonfield.fields.JSONField(default={})),
                ('duration', models.IntegerField(default=0)),
                ('class_actual', jsonfield.fields.JSONField(default={})),
                ('class_model',
                 models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                   related_name='class_trace_model', to='pred_models.PredModels')),
                ('reg_model',
                 models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                   related_name='reg_trace_model', to='pred_models.PredModels')),
                ('xlog', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='xlog',
                                           to='runtime.XLog')),
            ],
        ),
        migrations.AddField(
            model_name='xevent',
            name='trace',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                    related_name='xtrace', to='runtime.XTrace'),
        ),
    ]
