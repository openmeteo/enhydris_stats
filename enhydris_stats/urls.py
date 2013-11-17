from django.conf.urls import patterns, url

from enhydris_stats.views import HomeView

urlpatterns = patterns(
    '',

    url(r'^$', HomeView.as_view(), name='home'),
)
