# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wrtprices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='price_info',
            field=models.ForeignKey(related_name='+', to='wrtprices.PriceSummary', null=True),
        ),
        migrations.AlterField(
            model_name='priceoffer',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='pricesummary',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
