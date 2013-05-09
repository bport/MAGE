# coding: utf-8


from django.conf.urls import patterns, url
from scm import views

urlpatterns = patterns('',
    url(r'envts$', views.envts, name='envts'),
    url(r'envt/hist/(?P<envt_name>.*)', views.all_installs, name='envtinstallhist'),
    
    url(r'delivery$', views.delivery_list, name='deliveries'),
    url(r'delivery/(?P<iset_id>\d*)$', views.delivery, name='delivery_detail'),
    url(r'delivery/edit$', views.delivery_edit, name='delivery_create'),
    url(r'delivery/(?P<iset_id>\d*)/edit$', views.delivery_edit, name='delivery_edit'),
    url(r'delivery/(?P<iset_id>\d*)/validate$', views.delivery_validate, name='delivery_validate'),
    url(r'delivery/(?P<iset_id>\d*)/editdep$', views.delivery_edit_dep, name='delivery_edit_dep'),
    url(r'delivery/test/(?P<delivery_id>\d*)/(?P<envt_id>\d*)$', views.delivery_test, name='delivery_prereqs_test'),
    url(r'delivery/applyenvt/(?P<delivery_id>\d*)/(?P<envt_id>\d*)$', views.delivery_apply_envt, name='delivery_apply_envt'),
    url(r'delivery/lcapplyenvt$', views.lc_versions_per_environment, name='lc_installs_envts'),
    
    url(r'tag/create/(?P<envt_name>.*)/(?P<tag_name>.*)$', views.tag_create, name='tag_create'),
    url(r'tag/(?P<tag_id>\d*)$', views.tag_detail, name='tag_detail'),
    url(r'tag$', views.tag_list, name='tag_list'),
    
    url(r'bck/create/envtdefault/(?P<envt_name>.*)$', views.backup_envt, name='backup_envt'),
    url(r'bck/create/envtmanual/(?P<envt_name>.*)$', views.backup_envt_manual, name='backup_envt_manual'),
    url(r'bck/(?P<bck_id>\d*)$', views.backup_detail, name='backup_detail'),
    url(r'bck$', views.backup_list, name='backup_list'),
    
    url(r'demointernal', views.demo_internal, name='demointernal'),
    url(r'demo', views.demo, name='demo'),
    
    url(r'script/lcversions/(?P<lc_id>\d*)$', views.get_lc_versions, name='getlcversions'),         
)
