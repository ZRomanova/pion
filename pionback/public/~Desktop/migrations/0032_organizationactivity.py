# Generated by Django 2.0.2 on 2022-01-24 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0031_monitoringelement'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название вида деятельности организации')),
            ],
            options={
                'verbose_name_plural': 'Вид деятельности организации',
                'verbose_name': 'Вид деятельности организации',
            },
        ),
    ]