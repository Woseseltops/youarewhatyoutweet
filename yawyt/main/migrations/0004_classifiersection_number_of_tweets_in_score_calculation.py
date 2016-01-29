# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_classifiersection_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='classifiersection',
            name='number_of_tweets_in_score_calculation',
            field=models.IntegerField(default=30),
        ),
    ]
