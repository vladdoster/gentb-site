# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PipelineScriptsDirectory',
        ),
        migrations.AlterField(
            model_name='datasetscriptrun',
            name='dataset',
            field=models.ForeignKey(related_name='runs', to='predict.PredictDataset', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='datasetscriptrun',
            name='md5',
            field=models.CharField(db_index=True, max_length=40, blank=True),
        ),
        migrations.AlterField(
            model_name='predictdataset',
            name='user',
            field=models.ForeignKey(related_name='datasets', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='predictdatasetnote',
            name='dataset',
            field=models.ForeignKey(related_name='notes', to='predict.PredictDataset', on_delete=models.CASCADE),
        ),
    ]
