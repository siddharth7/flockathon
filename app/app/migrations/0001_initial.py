# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_userid', models.CharField(max_length=1000)),
                ('user_token', models.CharField(max_length=1000)),
                ('user_firstName', models.CharField(max_length=1000)),
                ('user_lastName', models.CharField(max_length=1000)),
                ('user_teamId', models.CharField(max_length=1000)),
            ],
        ),
    ]
