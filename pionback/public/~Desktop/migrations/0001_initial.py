# Generated by Django 3.0.8 on 2020-07-14 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Outcome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Общая формулировка социального результата')),
            ],
            options={
                'verbose_name': 'Социальный результат',
                'verbose_name_plural': 'Социальные результаты',
            },
        ),
        migrations.CreateModel(
            name='Practice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название практики')),
            ],
            options={
                'verbose_name': 'Практика',
                'verbose_name_plural': 'Практики',
            },
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название целевой группы')),
            ],
            options={
                'verbose_name': 'Целевая группа',
                'verbose_name_plural': 'Целевые группы',
            },
        ),
        migrations.CreateModel(
            name='OutcomeExactName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Частная формулировка социального результата')),
                ('outcome_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.Outcome')),
            ],
        ),
        migrations.AddField(
            model_name='outcome',
            name='practice_refs',
            field=models.ManyToManyField(blank=True, to='public.Practice', verbose_name='Практики'),
        ),
        migrations.AddField(
            model_name='outcome',
            name='target_refs',
            field=models.ManyToManyField(blank=True, to='public.Target', verbose_name='Целевые группы'),
        ),
    ]
