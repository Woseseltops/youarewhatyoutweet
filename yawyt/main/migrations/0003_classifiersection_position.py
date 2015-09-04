# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150815_0627'),
    ]

    operations = [
        migrations.AddField(
            model_name='classifiersection',
            name='position',
            field=models.IntegerField(default=0),
        ),
    ]
