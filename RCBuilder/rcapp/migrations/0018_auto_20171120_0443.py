# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-20 04:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rcapp', '0017_auto_20171119_2118'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='impact',
            options={'ordering': ['order'], 'verbose_name': 'Социальный эффект', 'verbose_name_plural': 'Социальные эффекты'},
        ),
        migrations.AlterModelOptions(
            name='outcome',
            options={'ordering': ['order'], 'verbose_name': 'Социальный результат', 'verbose_name_plural': 'Социальные результаты'},
        ),
        migrations.AlterModelOptions(
            name='output',
            options={'ordering': ['order'], 'verbose_name': 'Непосредственный результат', 'verbose_name_plural': 'Непосредственные результаты'},
        ),
    ]