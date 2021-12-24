from django.db.models import Sum, Count

from real_estate_api.ponude.models import Ponude
from real_estate_api.stanovi.models import Stanovi

def stanovi_report():
    queryset = Stanovi.objects.values("cena_stanaid_stana").annotate(
        total=Sum('cena_stana'),
        count=Count('cena_stana'),
        avg=Count('cena_stana')
    )
    return queryset
