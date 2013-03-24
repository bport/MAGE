# coding: utf-8

"""
    Graph module URL file.
    
    @author: Marc-Antoine Gouillart
    @contact: marsu_pilami@msn.com
    @license: GNU GVL v3
"""

from django.conf.urls import patterns,url
from gph import views

urlpatterns = patterns('',
    url(r'^full$',                                                               views.full_pic,    name='full'),
    url(r'^demo$',                                                               views.demo_pic,    name='demo'),
    url(r'filter/(?P<nbParents>\d*)/(?P<nbPartners>\d*)/(?P<collapseThr>\d*)',   views.filter_pic,  name='filter'),
    url(r'graph$',                                                               views.view_carto,  name='main'),
    url(r'envt/(?P<envt_id>\d*)/*$',                                             views.envt_pic,    name='envt'),
  # url(r'wk/(?P<wkf>.*)$',                                                      views.view_workflow, name='full'),                         
)