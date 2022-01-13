import json

from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.reverse import reverse

from real_estate_api.ponude.models import Ponude


class TestPonudeSerijalizers:
    """Tesritanje Serijalizers PONUDE"""

    def test_serializers_sve_ponude(self, client, nove_tri_ponude_fixture):
        """
        Testiranje serijalizera za pregled svih Ponuda sa fixtures od:
            * Tri kreirane nove Ponude.

        Testiranje se vrsi sa autorizovanim Korisnikom sistema (novi_jedan_auth_korisnik_fixture_ponude).

            * @see /test_ponude/conftest.py : nova_jedna_ponuda_fixture
            * @see /test_ponude/conftest.py : novi_jedan_auth_korisnik_fixture_ponude

        @param client: A Django test client instance.
        @param nove_tri_ponude_fixture: Ponuda
        @return status code 200: HTTP OK
        """
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

    def test_serializers_jedna_ponuda_401(self, client, nova_jedna_ponuda_fixture_401):
        """
        Testiranje serijalizera za pregled svih Ponuda sa fixtures od:
            * Jedne kreirane nove Ponude.

        Testiranje se vrsi sa NE autorizovanim Korisnikom sistema:
        -(novi_jedan_auth_korisnik_fixture_ponude).

            * @see /test_ponude/conftest.py : nova_jedna_ponuda_fixture
            * @see /test_ponude/conftest.py : novi_jedan_auth_korisnik_fixture_ponude

        @param client: A Django test client instance.
        @param nova_jedna_ponuda_fixture_401: Ponuda
        @return status code 401: HTTP Unauthorized.
        """
        response = client.get(reverse('ponude:lista_ponuda'))

        assert response.status_code == 401

        broj_ponuda = Ponude.objects.all().count()

        assert broj_ponuda == 1

    def test_invalid_serializers_detalji_jedne_ponude(self, client, nova_jedna_ponuda_fixture):
        """
        Testiranje serijalizera za pregled deatalja Ponude koji ne postoji,
        sa fixturom od:
            * Nove jedne Ponude (nova_jedna_ponuda_fixture)

        Testiranje se vrsi sa autorizovanim Korisnikom sistema (novi_jedan_auth_korisnik_fixture_ponude).

            * @see /test_ponude/conftest.py : nova_jedna_ponuda_fixture
            * @see /test_ponude/conftest.py : novi_jedan_auth_korisnik_fixture_ponude

        @param client: A Django test client instance.
        @param nova_jedna_ponuda_fixture: Ponuda
        @return status code 404: HTTP 404 Not Found
        """

        # Get invalid one Ponuda ID from Response.
        url_detalji_ponude = reverse('ponude:detalji_ponude',
                                     args=[nova_jedna_ponuda_fixture.id_ponude+ 1000])

        response = client.get(url_detalji_ponude)

        assert response.status_code == 404
