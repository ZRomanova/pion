# Generated by Django 2.0.2 on 2022-01-23 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0028_target_parent_ref'),
    ]

    operations = [
        migrations.CreateModel(
            name='Method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название метода')),
                ('add_public', models.BooleanField(default=True, verbose_name='Публичный доступ')),
                ('parent_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='public.Method', verbose_name='Родительский раздел')),
            ],
            options={
                'verbose_name_plural': 'Метод',
                'verbose_name': 'Метод',
            },
        ),
    ]
