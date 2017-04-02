# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20170401_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='user_firstName',
            field=models.CharField(default=datetime.datetime(2017, 4, 1, 13, 49, 26, 784685, tzinfo=utc), max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_lastName',
            field=models.CharField(default=datetime.datetime(2017, 4, 1, 13, 49, 29, 519163, tzinfo=utc), max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_teamId',
            field=models.CharField(default=datetime.datetime(2017, 4, 1, 13, 49, 31, 589447, tzinfo=utc), max_length=1000),
            preserve_default=False,
        ),
    ]
