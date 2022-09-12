# Generated by Django 2.0.2 on 2022-02-20 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0053_auto_20220218_2057'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseChangeRequest',
            fields=[
                ('name', models.CharField(default=None, max_length=500, null=True, verbose_name='Название кейса')),
                ('organization', models.CharField(default=None, max_length=500, null=True, verbose_name='Организация')),
                ('case_file', models.FileField(blank=True, default=None, null=True, upload_to='', verbose_name='Файл кейса')),
                ('url', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Ссылка на кейс')),
                ('verification_info', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Сведения о верификации практики, в рамках которой реализовывалась программа')),
                ('verification_level_regularity', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Регламентированность практики')),
                ('verification_level_validity', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Обоснованность практики')),
                ('verification_level_outcome_accessibility', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Достижение социальных результатов')),
                ('verification_level_outcome_validity', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Обоснованность данных о социальных результатах')),
                ('case_ref', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='public.Case')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата запроса')),
                ('add_public_confirm', models.BooleanField(default=False, verbose_name='Принять изменения')),
                ('monitoring_element_refs', models.ManyToManyField(blank=True, default=None, to='public.MonitoringElement', verbose_name='Элементы системы мониторинга и оценки')),
                ('organization_activity_refs', models.ManyToManyField(blank=True, default=None, to='public.OrganizationActivity', verbose_name='Виды деятельности')),
                ('practice_ref', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='public.Practice', verbose_name='Практика')),
                ('target_refs', models.ManyToManyField(blank=True, default=None, to='public.Target', verbose_name='Целевая группа')),
                ('thematic_group_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='public.ThematicGroup', verbose_name='Тематическая группа')),
            ],
            options={
                'verbose_name': 'Запрос на изменение кейса',
                'verbose_name_plural': 'Запрос на изменение кейса',
            },
        ),
        migrations.CreateModel(
            name='LogicalModelChangeRequest',
            fields=[
                ('name', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Название логической модели')),
                ('organization', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Организация')),
                ('period', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Сроки реализации')),
                ('verification_info', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Сведения о верификации практики, в рамках которой реализовывалась программа')),
                ('verification_level_regularity', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Регламентированность практики')),
                ('verification_level_validity', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Обоснованность практики')),
                ('verification_level_outcome_accessibility', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Достижение социальных результатов')),
                ('verification_level_outcome_validity', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Обоснованность данных о социальных результатах')),
                ('model_file', models.FileField(blank=True, default=None, null=True, upload_to='', verbose_name='Файл логической модели')),
                ('result_tree_file', models.FileField(blank=True, default=None, null=True, upload_to='', verbose_name='Файл дерева результатов')),
                ('logical_model_ref', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='public.LogicalModel')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата запроса')),
                ('add_public_confirm', models.BooleanField(default=False, verbose_name='Принять изменения')),
                ('outcome_refs', models.ManyToManyField(blank=True, default=None, to='public.Outcome', verbose_name='Социальные результаты')),
                ('practice_refs', models.ManyToManyField(blank=True, default=None, to='public.Practice', verbose_name='Практики')),
                ('target_refs', models.ManyToManyField(blank=True, default=None, to='public.Target', verbose_name='Целевые группы')),
                ('thematic_group_ref', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='public.ThematicGroup', verbose_name='Тематическая группа')),
            ],
            options={
                'verbose_name': 'Запрос на изменение логической модели',
                'verbose_name_plural': 'Запрос на изменение логической модели',
            },
        ),
        migrations.AlterModelOptions(
            name='toolchangerequest',
            options={'verbose_name': 'Запрос на изменение инструмента', 'verbose_name_plural': 'Запрос на изменение инструмента'},
        ),
        migrations.AddField(
            model_name='evaluationreport',
            name='add_public_confirm',
            field=models.BooleanField(default=True, verbose_name='Подтверждение администратором'),
        ),
        migrations.AddField(
            model_name='evaluationreport',
            name='add_public_will',
            field=models.BooleanField(default=False, verbose_name='Запрос сделать общедоступным'),
        ),
        migrations.AlterField(
            model_name='toolchangerequest',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата запроса'),
        ),
    ]