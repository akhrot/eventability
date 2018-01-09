from django.conf.urls import include, url
from . import views

app_name = 'events'

urlpatterns = [
	#url(r'^', views.index, name='index'),

    url(r'^$', views.homeview, name='homedefault'),
    url(r'^home/$', views.homeview, name='homeview'),
    url(r'^index/$', views.index, name='index'),
    url(r'^indexadmin/$', views.indexadmin, name='indexadmin'),
    url(r'^req_pending/$', views.req_pending, name='req_pending'),
    url(r'^req_history/$', views.req_history, name='req_history'),
    url(r'^req_status/$', views.req_status, name='req_status'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^login_admin/$', views.login_admin, name='login_admin'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<building_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<building_id>[0-9]+)/build_req/$', views.build_req, name='build_req'),
    url(r'^(?P<building_id>[0-9]+)/request_allot/$', views.request_allot, name='request_allot'),
    url(r'^(?P<allotment_id>[0-9]+)/req_accept/$', views.req_accept, name='req_accept'),
    url(r'^(?P<allotment_id>[0-9]+)/req_reject/$', views.req_reject, name='req_reject'),
    url(r'^access_denied/$', views.access_denied, name='access_denied'),
]