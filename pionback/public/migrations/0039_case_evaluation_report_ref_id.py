# Generated by Django 2.0.2 on 2022-01-31 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0038_auto_20220129_2318'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='evaluation_report_ref_id',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='public.EvaluationReport', verbose_name='Отчёт об оценке'),
        ),
    ]
