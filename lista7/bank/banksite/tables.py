from django_tables2 import tables

from banksite.models import Payment


class HistoryTable(tables.Table):
    class Meta:
        model = Payment
        template = 'django_tables2/bootstrap.html'
