from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',

    url(r'^$', 'enhydris_stats.views.home', name='home'),
)
