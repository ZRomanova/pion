# Generated by Django 2.0.2 on 2020-08-12 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0010_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='info',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Информация'),
        ),
    ]
