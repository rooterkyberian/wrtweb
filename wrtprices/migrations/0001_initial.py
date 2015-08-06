# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wrtprices.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('name', models.CharField(max_length=255, serialize=False,
                                          primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('hash', models.CharField(max_length=40, serialize=False,
                                          primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=255, null=True)),
                ('link', models.URLField()),
                ('status', models.CharField(max_length=255)),
                ('target', models.CharField(max_length=60)),
                ('platform', models.CharField(max_length=255)),
                ('cpu_speed', models.CharField(max_length=255)),
                ('flash', models.CharField(max_length=60)),
                ('ram', models.CharField(max_length=60)),
                ('wnic', models.CharField(max_length=255)),
                ('wireless', models.CharField(max_length=255)),
                ('wired', models.CharField(max_length=255)),
                ('usb', models.CharField(max_length=60)),
                ('other', models.TextField()),
                ('by', models.ForeignKey(to='wrtprices.Brand', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PriceOffer',
            fields=[
                ('hash', models.CharField(max_length=40, serialize=False,
                                          primary_key=True)),
                ('link', models.URLField()),
                ('price', wrtprices.models.MinMaxFloat()),
                ('price_with_shipping',
                 wrtprices.models.MinMaxFloat(null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(to='wrtprices.Device')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PriceSummary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('going_price', wrtprices.models.MinMaxFloat(null=True)),
                ('invalidated', models.BooleanField(default=False)),
                ('offers_count', models.IntegerField(default=0)),
                ('validated_offers_count', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(to='wrtprices.Device')),
                ('offers', models.ManyToManyField(to='wrtprices.PriceOffer')),
            ],
        ),
    ]
