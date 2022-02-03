import json

from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.reverse import reverse

from real_estate_api.lokali.ponude_lokala.test_ponude_lokala.conftest import *


class TestPonudeLokalaSerijalizers:
    """Testiranje Serijalizers PONUDE LOKALA"""

    def test_serializers_sve_ponude_lokala(self, client, nove_tri_ponude_lokala_fixture):
        """
        Testiranje serijalizera za pregled svih Ponuda Lokala sa fixturom od:
            * Tri kreirane nove Ponude Lokala.

        Testiranje se vrsi sa autorizovanim Korisnikom sistema (novi_autorizovan_korisnik_fixture_lokali_ponude).

            * @see /test_ponude_lokala/conftest.py : nove_tri_ponude_lokala_fixture
            * @see /test_ponude_lokala/conftest.py : novi_autorizovan_korisnik_fixture_lokali_ponude

        @param client: A Django test client instance.
        @param nove_tri_ponude_lokala_fixture: Ponuda Lokala
        @return status code 200: HTTP OK
        """
        response = client.get(reverse('ponude-lokali:lista_ponuda_lokala'))

        assert response.status_code == 200

        ponude_lokala = PonudeLokala.objects.all().order_by('id_ponude_lokala')
        broj_ponuda_lokala = PonudeLokala.objects.all().count()

        assert broj_ponuda_lokala == 3

        from real_estate_api.lokali.ponude_lokala.serializers import PonudeLokalaSerializer

        serializer = PonudeLokalaSerializer(ponude_lokala, many=True)

        ponude_iz_serializers = json.dumps(serializer.data, cls=DjangoJSONEncoder)

        ponude_iz_responsa = json.dumps(response.json()["results"])

        assert ponude_iz_serializers == ponude_iz_responsa

    def test_serializers_jedna_ponuda_401(self, client, nova_jedna_ponuda_lokala_fixture_401):
        """
        Testiranje serijalizera za pregled svih Ponuda Lokala sa fixtures od:
            * Jedne kreirane nove Ponude Lokala.

        Testiranje se vrsi sa NE autorizovanim Korisnikom sistema:
        -(novi_neautorizovan_korisnik_fixture_lokali_ponude).

            * @see /test_ponude_lokala/conftest.py : nova_jedna_ponuda_lokala_fixture_401
            * @see /test_ponude_lokala/conftest.py : novi_neautorizovan_korisnik_fixture_lokali_ponude

        @param client: A Django test client instance.
        @param nova_jedna_ponuda_lokala_fixture_401: Ponuda Lokala
        @return status code 401: HTTP Unauthorized.
        """
        response = client.get(reverse('ponude-lokali:lista_ponuda_lokala'))

        assert response.status_code == 401

        broj_ponuda_lokala = PonudeLokala.objects.all().count()

        assert broj_ponuda_lokala == 1

    def test_invalid_serializers_detalji_jedne_ponude_lokala(self, client, nova_jedna_ponuda_lokala_fixture):
        """
        Testiranje serijalizera za pregled deatalja Ponude Lokala koji ne postoji,
        sa fixturom od:
            * Nove jedne Ponude Lokala (nova_jedna_ponuda_lokala_fixture)

        Testiranje se vrsi sa autorizovanim Korisnikom sistema (novi_autorizovan_korisnik_fixture_lokali_ponude).

            * @see /test_ponude_lokala/conftest.py : nova_jedna_ponuda_lokala_fixture
            * @see /test_ponude_lokala/conftest.py : novi_autorizovan_korisnik_fixture_lokali_ponude

        @param client: A Django test client instance.
        @param nova_jedna_ponuda_lokala_fixture: Ponuda Lokala
        @return status code 404: HTTP 404 Not Found
        """
        # Get invalid one Ponuda Lokala ID from Response.
        url_detalji_ponude_lokala = reverse('ponude-lokali:detalji_ponude_lokala',
                                            args=[nova_jedna_ponuda_lokala_fixture.id_ponude_lokala + 1000])

        response = client.get(url_detalji_ponude_lokala)

        assert response.status_code == 404
