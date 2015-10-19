# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_auto_20151015_1401'),
    ]

    operations = [
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('source', models.CharField(max_length=50)),
                ('session', models.CharField(max_length=50)),
                ('upload', models.ForeignKey(to='frontend.Upload')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessId',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('processid', models.IntegerField()),
                ('process', models.ForeignKey(to='frontend.Process')),
            ],
        ),
    ]
