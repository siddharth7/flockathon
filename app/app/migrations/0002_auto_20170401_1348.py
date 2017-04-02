# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='user_firstName',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='user_lastName',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='user_teamId',
        ),
    ]
