from django.conf.urls import patterns, url

from enhydris_stats.views import HomeView

urlpatterns = patterns(
    '',

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^stations_list/$', 'enhydris_stats.views.stations_list',
        name='stations_list'),
)
