# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-05 03:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('introduction_to_models', '0003_auto_20170605_0333'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='teacher_type',
            new_name='teacher',
        ),
    ]