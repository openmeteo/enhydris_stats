from django.conf.urls import patterns, url

from enhydris_stats.views import HomeView, StationsListView

urlpatterns = patterns(
    '',

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^stations_list/$', StationsListView.as_view(), name='stations_list'),
)
