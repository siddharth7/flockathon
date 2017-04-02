# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20170401_1349'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('exp_paid', models.CharField(max_length=1000)),
                ('exp_for', models.CharField(max_length=1000)),
                ('exp_amount', models.CharField(max_length=1000)),
            ],
        ),
    ]
