from rest_framework import serializers
from rest_framework.reverse import reverse

from .views import Ponude


class PonudeSerializer(serializers.ModelSerializer):
    #absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Ponude
        fields = (
            'id_ponude',
            'kupac',
            'stan',
            'cena_stana_za_kupca',
            'napomena',
            'broj_ugovora',
            'datum_ugovora',
            'status_ponude',
            'nacin_placanja',
        )

        # TODO: Videti ovaj get_absolute_url
        # def get_absolute_url(self, obj):
        #     return reverse("lista_ponuda")
