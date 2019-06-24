from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^books$', views.main),
    url(r'^new_book$', views.new_book),
    url(r'^add_book$', views.add_book),
    url(r'^display_book/(?P<id>\d+)$', views.display_book)

]