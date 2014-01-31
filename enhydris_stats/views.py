from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView

from enhydris.hcore import models


class HomeView(TemplateView):
    template_name = 'enhydris_stats/index.html'

    def get_columns(self, base_queryset):
        result = [{
            'name': wd.id % 100,
            'value': base_queryset.filter(water_division__id=wd.id).count()
        } for wd in models.WaterDivision.objects.order_by('id')]
        result.append({'name': _(u'Total'), 'value': base_queryset.count()})
        return result

    def get(self, request, *args, **kwargs):
        try:
            years = [int(x) for x in request.GET.get('years', '').split(',')]
        except ValueError:
            years = []
        self.data = []
        for year in years:
            base_queryset = models.Gentity.objects.extra(
                where=["id in "
                       "(SELECT gentity_id FROM hcore_timeseries t "
                       "WHERE timeseries_end_date(t.id) >= '%s-01-01')"],
                params=[year])
            self.data.append({
                'heading': _('Number of stations with data for {0} or later'
                             ).format(year),
                'columns': self.get_columns(base_queryset),
            })
        self.data.append({
            'heading': _('Number of stations in database'),
            'columns': self.get_columns(models.Station.objects),
        })
        return super(HomeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['data'] = self.data
        return context


class StationsListView(TemplateView):
    template_name = 'enhydris_stats/stations_list.html'

    def get_context_data(self, **kwargs):
        context = super(StationsListView, self).get_context_data(**kwargs)
        context['stations'] = self._get_stations()
        return context

    def _get_stations(self):
        all_stations = models.Gentity.objects.all()
        stations = []
        for station in all_stations:
            variables = {}  # Variable name to end year mapping
            ts = models.Timeseries.objects.filter(gentity=station).extra(
                select={'t_end_date': 'timeseries_end_date(id)'},
                where=['timeseries_end_date(id) IS NOT NULL'])
            for t in ts:
                variables[t.variable.descr] = max(
                    t.t_end_date.year, variables.get(t.variable.descr, 0))
            station.variables = []
            for v in variables:
                station.variables.append({'name': v, 'end_year': variables[v]})
            if variables:
                stations.append(station)
        return stations
