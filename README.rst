``enhydris_stats`` is an add-on to Enhydris that shows various
statistics about numbers of stations in the database.

Installation
============

 1. Put ``enhydris_stats`` in your Python path.

 2. Add ``enhydris_stats`` to ``INSTALLED_APPS`` in your ``settings.py``.

 3. Add ``enhydris_stats`` to your ``urls.py``::

       urlpatterns += patterns(
          '',
          (r'^stats/', include('enhydris_stats.urls')),
        )
