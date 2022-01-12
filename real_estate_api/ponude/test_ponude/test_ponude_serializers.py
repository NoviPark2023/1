import json

from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.reverse import reverse

from real_estate_api.ponude.models import Ponude


class TestPonudeSerijalizers:
    """Tesritanje Serijalizers PONUDE"""

    def test_serializers_sve_ponude(self, client, nove_tri_ponude_fixture):
        response = client.get(reverse('ponude:lista_ponuda'))

        assert response.status_code == 200

        ponude = Ponude.objects.all().order_by('id_ponude')
        broj_ponuda = Ponude.objects.all().count()

        assert broj_ponuda == 3

        from real_estate_api.ponude.serializers import PonudeSerializer

        serializer = PonudeSerializer(ponude, many=True)

        ponude_iz_seralizer = json.dumps(serializer.data, cls=DjangoJSONEncoder)

        ponude_is_responsa = json.dumps(response.json()["results"])


        assert ponude_iz_seralizer == ponude_is_responsa
