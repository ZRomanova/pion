# Generated by Django 2.0.2 on 2022-01-24 11:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('public', '0034_tool'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название вида деятельности организации')),
                ('add_public', models.BooleanField(default=True, verbose_name='Публичный доступ')),
            ],
            options={
                'verbose_name_plural': 'Вид деятельности организации',
                'verbose_name': 'Вид деятельности организации',
            },
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название кейса')),
                ('organization', models.CharField(max_length=500, verbose_name='Организация')),
                ('case_file', models.FileField(blank=True, default=None, null=True, upload_to='', verbose_name='Файл кейса')),
                ('verification_info', models.CharField(blank=True, default='', max_length=2000, verbose_name='Сведения о верификации практики, в рамках которой реализовывалась программа')),
                ('verification_level_regularity', models.CharField(blank=True, default='', max_length=2000, verbose_name='Регламентированность практики')),
                ('verification_level_validity', models.CharField(blank=True, default='', max_length=2000, verbose_name='Обоснованность практики')),
                ('verification_level_outcome_accessibility', models.CharField(blank=True, default='', max_length=2000, verbose_name='Достижение социальных результатов')),
                ('verification_level_outcome_validity', models.CharField(blank=True, default='', max_length=2000, verbose_name='Обоснованность данных о социальных результатах')),
                ('add_public_will', models.BooleanField(default=False, verbose_name='В общую библиотеку')),
                ('add_public_confirm', models.BooleanField(default=False, verbose_name='Подтверждение администратором ')),
                ('createdby', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Кейсы',
                'verbose_name': 'Кейсы',
            },
        ),
        migrations.CreateModel(
            name='CaseLibraryLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.Case', verbose_name='Кейс')),
                ('user_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Связи кейсов с личной библиотекой',
                'verbose_name': 'Связь кейса с личной библиотекой',
            },
        ),
        migrations.CreateModel(
            name='EvaluationReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=500, verbose_name='Тип отчета')),
                ('evaluation_type', models.CharField(max_length=500, verbose_name='evaluation_type')),
                ('key_questions', models.CharField(max_length=2000, verbose_name='Ключевые вопросы')),
                ('other_results', models.CharField(max_length=2000, verbose_name='Другие результаты')),
                ('analysis_method_refs', models.ManyToManyField(to='public.AnalysisMethod', verbose_name='Методы анализа данных')),
            ],
            options={
                'verbose_name_plural': 'Oтчёт об оценке',
                'verbose_name': 'Oтчёт об оценке',
            },
        ),
        migrations.CreateModel(
            name='EvaluationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название вида деятельности организации')),
                ('add_public', models.BooleanField(default=True, verbose_name='Публичный доступ')),
            ],
            options={
                'verbose_name_plural': 'Вид деятельности организации',
                'verbose_name': 'Вид деятельности организации',
            },
        ),
        migrations.CreateModel(
            name='RepresentationMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название вида деятельности организации')),
                ('add_public', models.BooleanField(default=True, verbose_name='Публичный доступ')),
            ],
            options={
                'verbose_name_plural': 'Вид деятельности организации',
                'verbose_name': 'Вид деятельности организации',
            },
        ),
        migrations.CreateModel(
            name='ToolLibraryLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Связи инструментов с личной библиотекой',
                'verbose_name': 'Связь инструмента с личной библиотекой',
            },
        ),
        migrations.AddField(
            model_name='tool',
            name='add_public_confirm',
            field=models.BooleanField(default=False, verbose_name='Подтверждение администратором '),
        ),
        migrations.AddField(
            model_name='tool',
            name='add_public_will',
            field=models.BooleanField(default=False, verbose_name='В общую библиотеку'),
        ),
        migrations.AddField(
            model_name='tool',
            name='createdby',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='toollibrarylink',
            name='tool_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.Tool', verbose_name='Инструмент'),
        ),
        migrations.AddField(
            model_name='toollibrarylink',
            name='user_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='evaluationreport',
            name='evaluation_type_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.EvaluationType', verbose_name='Вид оценки'),
        ),
        migrations.AddField(
            model_name='evaluationreport',
            name='method_refs',
            field=models.ManyToManyField(blank=True, to='public.Method', verbose_name='Методы'),
        ),
        migrations.AddField(
            model_name='evaluationreport',
            name='outcome_refs',
            field=models.ManyToManyField(to='public.Outcome', verbose_name='Социальные результаты'),
        ),
        migrations.AddField(
            model_name='evaluationreport',
            name='representation_refs',
            field=models.ManyToManyField(to='public.RepresentationMethod', verbose_name='Методы представления данных в отчете'),
        ),
        migrations.AddField(
            model_name='case',
            name='monitoring_element_refs',
            field=models.ManyToManyField(blank=True, to='public.MonitoringElement', verbose_name='Элементы системы мониторинга и оценки'),
        ),
        migrations.AddField(
            model_name='case',
            name='organization_activity_refs',
            field=models.ManyToManyField(blank=True, to='public.OrganizationActivity', verbose_name='Виды деятельности'),
        ),
        migrations.AddField(
            model_name='case',
            name='practice_ref',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='public.Practice', verbose_name='Практика'),
        ),
        migrations.AddField(
            model_name='case',
            name='target_refs',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='public.Target', verbose_name='Целевая группа'),
        ),
        migrations.AddField(
            model_name='case',
            name='thematic_group_ref',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='public.ThematicGroup', verbose_name='Тематическая группа'),
        ),
    ]
