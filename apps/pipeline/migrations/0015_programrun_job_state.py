# Generated by Django 2.2.13 on 2020-12-14 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0014_remove_program_keep'),
    ]

    operations = [
        migrations.AddField(
            model_name='programrun',
            name='job_state',
            field=models.CharField(blank=True, choices=[(None, 'Status not requested'), ('', 'Unknown State (non returned)'), ('OUT_OF_MEMORY', 'Out of Memory'), ('TIMEOUT', 'Timeout'), ('CANCELLED', 'Cancelled'), ('FAILED', 'Failed'), ('COMPLETED', 'Completed')], db_index=True, max_length=16, null=True),
        ),
    ]
