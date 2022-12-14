# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-31 04:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rcapp', '0028_helpparagraph_special_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='target_ref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rcapp.Target'),
        ),
        migrations.AddField(
            model_name='impact',
            name='outcome_ref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rcapp.Outcome'),
        ),
    ]
