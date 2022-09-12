# Generated by Django 2.0.2 on 2020-08-28 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0014_monitoringformlineimpact_monitoringformlinemidoutcome_monitoringformlineoutput_monitoringformlinesho'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitoringformlineimpact',
            name='mpl_ref',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='public.MonitoringPlanLineImpact', verbose_name='Строка плана мониторинга'),
        ),
        migrations.AddField(
            model_name='monitoringformlinemidoutcome',
            name='mpl_ref',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='public.MonitoringPlanLineMidOutcome', verbose_name='Строка плана мониторинга'),
        ),
        migrations.AddField(
            model_name='monitoringformlineoutput',
            name='mpl_ref',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='public.MonitoringPlanLineOutput', verbose_name='Строка плана мониторинга'),
        ),
        migrations.AddField(
            model_name='monitoringformlineshortoutcome',
            name='mpl_ref',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='public.MonitoringPlanLineShortOutcome', verbose_name='Строка плана мониторинга'),
        ),
    ]