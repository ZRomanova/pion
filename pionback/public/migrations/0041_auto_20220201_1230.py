# Generated by Django 2.0.2 on 2022-02-01 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0040_remove_case_evaluation_report_ref_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='createdby',
        ),
        migrations.RemoveField(
            model_name='case',
            name='monitoring_element_refs',
        ),
        migrations.RemoveField(
            model_name='case',
            name='organization_activity_refs',
        ),
        migrations.RemoveField(
            model_name='case',
            name='practice_ref',
        ),
        migrations.RemoveField(
            model_name='case',
            name='target_refs',
        ),
        migrations.RemoveField(
            model_name='case',
            name='thematic_group_ref',
        ),
        migrations.RemoveField(
            model_name='caselibrarylink',
            name='case_ref',
        ),
        migrations.RemoveField(
            model_name='caselibrarylink',
            name='user_ref',
        ),
        migrations.RemoveField(
            model_name='evaluationreport',
            name='analysis_method_refs',
        ),
        migrations.RemoveField(
            model_name='evaluationreport',
            name='case_ref',
        ),
        migrations.RemoveField(
            model_name='evaluationreport',
            name='evaluation_type_ref',
        ),
        migrations.RemoveField(
            model_name='evaluationreport',
            name='method_refs',
        ),
        migrations.RemoveField(
            model_name='evaluationreport',
            name='outcome_refs',
        ),
        migrations.RemoveField(
            model_name='evaluationreport',
            name='representation_method_refs',
        ),
        migrations.DeleteModel(
            name='Case',
        ),
        migrations.DeleteModel(
            name='CaseLibraryLink',
        ),
        migrations.DeleteModel(
            name='EvaluationReport',
        ),
    ]
