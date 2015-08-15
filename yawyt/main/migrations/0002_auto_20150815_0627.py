# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classifiersection',
            old_name='classifier_name',
            new_name='classifier_class_name',
        ),
        migrations.AddField(
            model_name='classifiersection',
            name='classifier_module_name',
            field=models.CharField(default='hoi', max_length=200),
            preserve_default=False,
        ),
    ]
