# Generated by Django 2.0.2 on 2022-01-24 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0032_organizationactivity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='toolsitem',
            name='creator',
        ),
        migrations.DeleteModel(
            name='ToolsItem',
        ),
    ]
