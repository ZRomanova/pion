# Generated by Django 2.0.2 on 2020-08-12 02:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0011_auto_20200812_0141'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramImpact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название социального эффекта')),
                ('info', models.TextField(blank=True, default=None, null=True, verbose_name='Информация')),
            ],
            options={
                'verbose_name_plural': 'Социальные эффекты',
                'verbose_name': 'Социальный эффект',
            },
        ),
        migrations.CreateModel(
            name='ProgramMidOutcome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название среднесрочного социального результата')),
                ('info', models.TextField(blank=True, default=None, null=True, verbose_name='Информация')),
                ('outcome_ref', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='public.Outcome', verbose_name='Социальный результат из библиотеки')),
                ('program_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.Program', verbose_name='Программа')),
            ],
            options={
                'verbose_name_plural': 'Среднесрочные социальные результаты',
                'verbose_name': 'Среднесрочный социальный результат',
            },
        ),
        migrations.CreateModel(
            name='ProgramOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название непосредственного результата')),
                ('info', models.TextField(blank=True, default=None, null=True, verbose_name='Информация')),
                ('activity_ref', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='public.Activity', verbose_name='Активность')),
                ('program_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.Program', verbose_name='Программа')),
            ],
            options={
                'verbose_name_plural': 'Непосредственные результаты',
                'verbose_name': 'Непосредственный результат',
            },
        ),
        migrations.CreateModel(
            name='ProgramShortOutcome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название краткосрочного социального результата')),
                ('info', models.TextField(blank=True, default=None, null=True, verbose_name='Информация')),
                ('outcome_ref', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='public.Outcome', verbose_name='Социальный результат из библиотеки')),
                ('program_output_ref', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='public.ProgramOutput', verbose_name='Непосредственный результат')),
                ('program_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.Program', verbose_name='Программа')),
            ],
            options={
                'verbose_name_plural': 'Краткосрочные социальные результаты',
                'verbose_name': 'Краткосрочный социальный результат',
            },
        ),
        migrations.AddField(
            model_name='programmidoutcome',
            name='program_short_outcome_ref',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='public.ProgramShortOutcome', verbose_name='Краткосрочный социальный результат'),
        ),
        migrations.AddField(
            model_name='programimpact',
            name='program_mid_outcome_ref',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='public.ProgramMidOutcome', verbose_name='Среднесрочный социальный результат'),
        ),
        migrations.AddField(
            model_name='programimpact',
            name='program_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.Program', verbose_name='Программа'),
        ),
    ]
