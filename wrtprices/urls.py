# -*- coding: UTF-8 -*-

# Copyright (c) 2015 Maciej Urbański <rooter@kyberian.net>

from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'devices', views.DeviceViewSet)
router.register(r'price_summaries', views.PriceSummaryViewSet)

urlpatterns = [
    url(r'^$', views.devices, name='devices'),
    url(r'^api/v1/', include(router.urls)),
]
