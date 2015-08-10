# -*- coding: UTF-8 -*-

# Copyright (c) 2015 Maciej Urbański <rooter@kyberian.net>

from django.conf.urls import url, include
from django.views.generic import TemplateView
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'devices', views.DeviceViewSet)
router.register(r'price_summaries', views.PriceSummaryViewSet)

urlpatterns = [
    url(r'^$', views.devices, name='devices'),
    url(r'^toh$', TemplateView.as_view(template_name="devices_index.html")),
    url(r'^api/v1/', include(router.urls)),
]
