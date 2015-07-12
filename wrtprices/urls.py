# -*- coding: UTF-8 -*-

# Copyright (c) 2015 Maciej Urbański <rooter@kyberian.net>

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.devices, name='devices'),
]
