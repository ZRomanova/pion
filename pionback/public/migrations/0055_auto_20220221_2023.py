# Generated by Django 2.0.2 on 2022-02-21 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0054_auto_20220220_1957'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvaluationReportChangeRequest',
            fields=[
                ('type', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Тип отчета')),
                ('key_questions', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Ключевые вопросы')),
                ('other_results', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Другие результаты')),
                ('evaluation_file', models.FileField(blank=True, default=None, null=True, upload_to='', verbose_name='Файл отчёта')),
                ('evalution_report_ref', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='public.EvaluationReport')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата запроса')),
                ('add_public_confirm', models.BooleanField(default=False, verbose_name='Принять изменения')),
                ('analysis_method_refs', models.ManyToManyField(blank=True, to='public.AnalysisMethod', verbose_name='Методы анализа данных')),
                ('evaluation_type_ref', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='public.EvaluationType', verbose_name='Вид оценки')),
                ('method_refs', models.ManyToManyField(blank=True, to='public.Method', verbose_name='Методы')),
                ('outcome_refs', models.ManyToManyField(blank=True, to='public.Outcome', verbose_name='Социальные результаты')),
                ('representation_method_refs', models.ManyToManyField(blank=True, to='public.RepresentationMethod', verbose_name='Методы представления данных в отчете')),
            ],
            options={
                'verbose_name_plural': 'Запрос на редактирование отчёта об оценке',
                'verbose_name': 'Запрос на редактирование отчёта об оценке',
            },
        ),
        migrations.AlterField(
            model_name='evaluationreport',
            name='evaluation_type_ref',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='public.EvaluationType', verbose_name='Вид оценки'),
        ),
        migrations.AlterField(
            model_name='evaluationreport',
            name='key_questions',
            field=models.CharField(default='', max_length=2000, verbose_name='Ключевые вопросы'),
        ),
        migrations.AlterField(
            model_name='evaluationreport',
            name='other_results',
            field=models.CharField(default='', max_length=2000, verbose_name='Другие результаты'),
        ),
    ]
