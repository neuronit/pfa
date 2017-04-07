

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='play'),
#    url(r'^save/$', views.save, name='save'),
    url(r'^result/$', views.result, name='result'),
    url(r'^result_network/$',views.result_network, name='result_network'),
    ]
