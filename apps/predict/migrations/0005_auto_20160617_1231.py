# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0004_auto_20160613_1047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='predictdataset',
            name='status',
        ),
        migrations.AlterField(
            model_name='scripttorun',
            name='script',
            field=models.TextField(help_text=b'Example of JSON argument: \'{"admin_url": "http://127.0.0.1:8000/tb-admin/predict/PredictDataset/3/", "callback_url": "some_url to receive results", "dataset_id": 3, "user_email": "user_who_uploaded_file@place.edu", "file1_path": ".../tb_uploaded_files/shared-files/2015/08/Predict_-_genTB_BnVjFcO.png"}\'', verbose_name=b'Command Line Script'),
        ),
    ]
