# Generated by Django 2.0.2 on 2022-02-01 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0042_case_caselibrarylink_evaluationreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tool',
            name='method_ref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='public.Method', verbose_name='Метод'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='outcome_level_ref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='public.OutcomeLevel', verbose_name='Уровень социального результата'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='outcome_ref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='public.Outcome', verbose_name='Социальный результат'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='practice_ref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='public.Practice', verbose_name='Практика'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='thematic_group_ref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='public.ThematicGroup', verbose_name='Тематическая группа'),
        ),
    ]
