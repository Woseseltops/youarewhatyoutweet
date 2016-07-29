# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_classifiersection_number_of_tweets_in_score_calculation'),
    ]

    operations = [
        migrations.AddField(
            model_name='classifiersection',
            name='number_of_tweets_to_analyze',
            field=models.IntegerField(help_text='0 = everything', default=0),
        ),
        migrations.AlterField(
            model_name='classifiersection',
            name='number_of_tweets_in_score_calculation',
            field=models.IntegerField(help_text='0 = everything', default=30),
        ),
    ]
