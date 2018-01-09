# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_allotment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='allotment',
            name='event',
            field=models.CharField(default='code.fun.do', max_length=250),
            preserve_default=False,
        ),
    ]
