# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-19 16:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rcapp', '0012_outcomeindicatorpf_outputindicatorpf'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='outcomeindicatorpf',
            options={'verbose_name': 'План и факт показателя социального результата', 'verbose_name_plural': 'Планы и факты показателя социального результата'},
        ),
        migrations.AlterModelOptions(
            name='outputindicatorpf',
            options={'verbose_name': 'План и факт показателя непосредственного результата', 'verbose_name_plural': 'Планы и факты показателя непосредственного результата'},
        ),
    ]