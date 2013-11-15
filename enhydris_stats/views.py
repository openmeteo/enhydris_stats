from django.shortcuts import render_to_response
from django.template import RequestContext

from enhydris.hcore import models


def home(request):
    try:
        years = [int(x) for x in request.GET.get('years', '').split(',')]
    except ValueError:
        years = []
    data = []
    for year in years:
        dataitem = {'year': year}
        dataitem['nstations'] = models.Gentity.objects.extra(
            where=["id in "
                   "(SELECT gentity_id FROM hcore_timeseries t "
                   "WHERE timeseries_end_date(t.id) >= '%s-01-01')"],
            params=[year]).count()
        data.append(dataitem)
    return render_to_response('enhydris_stats/index.html',
                              {'data': data,
                               'nstations': models.Station.objects.count(),
                               },
                              context_instance=RequestContext(request))
