# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Allotment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('allot_date', models.DateField()),
                ('club', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('capacity', models.IntegerField()),
                ('desc', models.CharField(max_length=1000)),
                ('build_img', models.FileField(upload_to=b'')),
            ],
        ),
        migrations.AddField(
            model_name='allotment',
            name='building',
            field=models.ForeignKey(to='events.Building'),
        ),
    ]
