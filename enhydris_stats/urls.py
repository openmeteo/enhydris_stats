from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',

    url(r'^$', 'enhydris_stats.views.home', name='home'),
    url(r'^stations_list/$', 'enhydris_stats.views.stations_list',
        name='stations_list'),
)
