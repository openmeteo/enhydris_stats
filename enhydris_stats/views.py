from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from enhydris.hcore import models


def get_columns(base_queryset):
    result = [{'name': wd.id % 100,
               'value': base_queryset.filter(water_division__id=wd.id).count()}
              for wd in models.WaterDivision.objects.order_by('id')]
    result.append({'name': _(u'Total'), 'value': base_queryset.count()})
    return result


def home(request):
    try:
        years = [int(x) for x in request.GET.get('years', '').split(',')]
    except ValueError:
        years = []
    data = []
    for year in years:
        base_queryset = models.Gentity.objects.extra(
            where=["id in "
                   "(SELECT gentity_id FROM hcore_timeseries t "
                   "WHERE timeseries_end_date(t.id) >= '%s-01-01')"],
            params=[year])
        data.append({
            'heading': _('Number of stations with data for {0} or later'
                         ).format(year),
            'columns': get_columns(base_queryset),
        })
    data.append({
        'heading': _('Number of stations in database'),
        'columns': get_columns(models.Station.objects),
    })
    return render_to_response('enhydris_stats/index.html',
                              {'data': data},
                              context_instance=RequestContext(request))


def stations_list(request):
    stations = models.Gentity.objects.extra(
        where=["id in "
               "(SELECT gentity_id FROM hcore_timeseries t "
               "WHERE timeseries_end_date(t.id) IS NOT NULL)"])
    for station in stations:
        station.variables = []
        for t in models.Timeseries.objects.filter(gentity=station).extra(
                where=["timeseries_end_date(id) IS NOT NULL"]):
            if t.variable.descr not in station.variables:
                station.variables.append(t.variable.descr)
        station.variables.sort()
    return render_to_response('enhydris_stats/stations_list.html',
                              {'stations': stations},
                              context_instance=RequestContext(request))
