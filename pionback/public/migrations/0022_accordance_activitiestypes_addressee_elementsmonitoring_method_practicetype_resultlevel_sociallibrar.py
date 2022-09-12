# Generated by Django 2.0.2 on 2022-01-20 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0021_auto_20210506_1933'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accordance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('parent_group', models.BooleanField(default=False, verbose_name='Родительский раздел')),
                ('library_type', models.CharField(choices=[('TYPE_TOOLS', 'Библиотека инструментов'), ('TYPE_CASE', 'Библиотека кейсов'), ('TYPE_ALL', 'Все библиотеки')], default='TYPE_ALL', max_length=100, verbose_name='Тип библиотеки')),
            ],
            options={
                'verbose_name': 'Данные о верификации практики на соответствие Стандарту доказательности практик  в сфере детства',
                'verbose_name_plural': 'Данные о верификации практики на соответствие Стандарту доказательности практик  в сфере детства',
            },
        ),
        migrations.CreateModel(
            name='ActivitiesTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('parent_group', models.BooleanField(default=False, verbose_name='Родительский раздел')),
                ('library_type', models.CharField(choices=[('TYPE_TOOLS', 'Библиотека инструментов'), ('TYPE_CASE', 'Библиотека кейсов'), ('TYPE_ALL', 'Все библиотеки')], default='TYPE_ALL', max_length=100, verbose_name='Тип библиотеки')),
            ],
            options={
                'verbose_name': 'Виды деятельности (активностей) организации, представленные в кейсе',
                'verbose_name_plural': 'Виды деятельности (активностей) организации, представленные в кейсе',
            },
        ),
        migrations.CreateModel(
            name='Addressee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('parent_group', models.BooleanField(default=False, verbose_name='Родительский раздел')),
                ('library_type', models.CharField(choices=[('TYPE_TOOLS', 'Библиотека инструментов'), ('TYPE_CASE', 'Библиотека кейсов'), ('TYPE_ALL', 'Все библиотеки')], default='TYPE_ALL', max_length=100, verbose_name='Тип библиотеки')),
            ],
            options={
                'verbose_name': 'Целевая группа/адресат',
                'verbose_name_plural': 'Целевая группа/адресат',
            },
        ),
        migrations.CreateModel(
            name='ElementsMonitoring',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('parent_group', models.BooleanField(default=False, verbose_name='Родительский раздел')),
                ('library_type', models.CharField(choices=[('TYPE_TOOLS', 'Библиотека инструментов'), ('TYPE_CASE', 'Библиотека кейсов'), ('TYPE_ALL', 'Все библиотеки')], default='TYPE_ALL', max_length=100, verbose_name='Тип библиотеки')),
            ],
            options={
                'verbose_name': 'Элементы системы мониторинга и оценки, представленные в кейсе',
                'verbose_name_plural': 'Элементы системы мониторинга и оценки, представленные в кейсе',
            },
        ),
        migrations.CreateModel(
            name='Method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('parent_group', models.BooleanField(default=False, verbose_name='Родительский раздел')),
                ('library_type', models.CharField(choices=[('TYPE_TOOLS', 'Библиотека инструментов'), ('TYPE_CASE', 'Библиотека кейсов'), ('TYPE_ALL', 'Все библиотеки')], default='TYPE_ALL', max_length=100, verbose_name='Тип библиотеки')),
            ],
            options={
                'verbose_name': 'Метод',
                'verbose_name_plural': 'Метод',
            },
        ),
        migrations.CreateModel(
            name='PracticeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('parent_group', models.BooleanField(default=False, verbose_name='Родительский раздел')),
                ('library_type', models.CharField(choices=[('TYPE_TOOLS', 'Библиотека инструментов'), ('TYPE_CASE', 'Библиотека кейсов'), ('TYPE_ALL', 'Все библиотеки')], default='TYPE_ALL', max_length=100, verbose_name='Тип библиотеки')),
            ],
            options={
                'verbose_name': 'Тип практики',
                'verbose_name_plural': 'Тип практики',
            },
        ),
        migrations.CreateModel(
            name='ResultLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('parent_group', models.BooleanField(default=False, verbose_name='Родительский раздел')),
                ('library_type', models.CharField(choices=[('TYPE_TOOLS', 'Библиотека инструментов'), ('TYPE_CASE', 'Библиотека кейсов'), ('TYPE_ALL', 'Все библиотеки')], default='TYPE_ALL', max_length=100, verbose_name='Тип библиотеки')),
            ],
            options={
                'verbose_name': 'Уровень результата',
                'verbose_name_plural': 'Уровень результата',
            },
        ),
        migrations.CreateModel(
            name='SocialLibraryPEON',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('parent_group', models.BooleanField(default=False, verbose_name='Родительский раздел')),
                ('library_type', models.CharField(choices=[('TYPE_TOOLS', 'Библиотека инструментов'), ('TYPE_CASE', 'Библиотека кейсов'), ('TYPE_ALL', 'Все библиотеки')], default='TYPE_ALL', max_length=100, verbose_name='Тип библиотеки')),
            ],
            options={
                'verbose_name': 'Социальный результат из библиотеки ПИОНа',
                'verbose_name_plural': 'Социальный результат из библиотеки ПИОНа',
            },
        ),
        migrations.CreateModel(
            name='ThematicGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('parent_group', models.BooleanField(default=False, verbose_name='Родительский раздел')),
                ('library_type', models.CharField(choices=[('TYPE_TOOLS', 'Библиотека инструментов'), ('TYPE_CASE', 'Библиотека кейсов'), ('TYPE_ALL', 'Все библиотеки')], default='TYPE_ALL', max_length=100, verbose_name='Тип библиотеки')),
            ],
            options={
                'verbose_name': 'Тематическая группа',
                'verbose_name_plural': 'Тематическая группа',
            },
        ),
    ]