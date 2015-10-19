# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_testfile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TestFile',
        ),
        migrations.AlterField(
            model_name='audiofile',
            name='audiofile',
            field=models.FileField(upload_to=b'/Users/jeremychristian/Documents/project/server/storage/audiofiles'),
        ),
        migrations.AlterField(
            model_name='upload',
            name='metadata',
            field=models.FileField(upload_to=b'/Users/jeremychristian/Documents/project/server/storage/metadata'),
        ),
        migrations.AlterField(
            model_name='upload',
            name='transcripts',
            field=models.FileField(upload_to=b'/Users/jeremychristian/Documents/project/server/storage/transcripts'),
        ),
    ]
