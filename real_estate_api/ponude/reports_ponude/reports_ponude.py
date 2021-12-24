from django.db.models import Sum, Count

from real_estate_api.ponude.models import Ponude
from real_estate_api.stanovi.models import Stanovi

def ponude_report():

    data = []

    queryset = Ponude.objects.all().values("id_ponude").annotate(
        total=Sum('cena_stana_za_kupca'),
        count=Count('cena_stana_za_kupca'),
        avg=Count('cena_stana_za_kupca')
    )

    return queryset

