# Generated by Django 2.0.2 on 2021-06-10 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20210116_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainform',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Телефон'),
        ),
    ]
