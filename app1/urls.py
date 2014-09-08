# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'app1.views',
    url(r'^$', 'ma_list', name='ma_list'),
    url(r'^add/$', 'ma_create', name='ma_create'),
    url(r'^(?P<pk>\d+)/$', 'ma_detail', name='ma_detail'),
    url(r'^(?P<pk>\d+)/delete/$', 'ma_delete', name='ma_delete'),
    url(r'^(?P<pk>\d+)/edit/$', 'ma_update', name='ma_update'),
    url(r'^(?P<pk>\d+)/history/$', 'get_history_ModelA', name='ma_history'),
    url(r'^(?P<pk>\d+)/revert/(?P<rev_pk>\d+)/$', 'revert_modela_to_revision',
        name='ma_revert'),
)
