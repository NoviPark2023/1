import json

from rest_framework.reverse import reverse

from real_estate_api.korisnici.models import Korisnici


class TestKorisniciSerijalizers:
    """Tesritanje Serijalizers KORISNICI"""

    def test_serializers_svi_korisnici(self, client, nova_tri_korisnika_fixture, novi_jedan_auth_korisnik_fixture):
        """
        Testiranje serijalizera za pregled svih Korisnika sa fixtures od:
            * Tri kreirana nova obicna Korisnika.
            * Jednog SuperUser Korisnika.

        Testiranje se vrsi sa autorizovanim Korisnikom sistema (novi_jedan_auth_korisnik_fixture).

            * @see /test_korisnici/conftest.py (nova_tri_korisnika_fixture)
            * @see /test_korisnici/conftest.py (novi_jedan_auth_korisnik_fixture)

        @param client: A Django test client instance.
        @param nova_tri_korisnika_fixture: Tri obicna Korisnika
        @param novi_jedan_auth_korisnik_fixture: SuperUser Korisnik
        @return status code 200: HTTP OK
        """

        response = client.get(reverse('korisnici:lista_korisnika'))

        korisnici = Korisnici.objects.all().order_by('id')
        broj_korisnika = Korisnici.objects.all().count()

        assert response.status_code == 200

        # Provea broja Korisnika (4).
        # Imamo jednog SuperUser-a (novi_jedan_auth_korisnik_fixture)
        # Imamo tri obicna Korisnika (nova_tri_korisnika_fixture)
        assert broj_korisnika == 4

        # Lokalno import 'KorisniciSerializers'.
        from real_estate_api.korisnici.serializers import KorisniciSerializers

        serializer = KorisniciSerializers(korisnici, many=True)

        print(f'RESPONSE DATA: {json.dumps(serializer.data)}')
        print(f'RESPONSE DATA: {response.json()}')

        assert json.dumps(serializer.data) == json.dumps(response.json())

    def test_invalid_serializers_detalji_jednog_korisnika(self,
                                                          client,
                                                          nova_tri_korisnika_fixture,
                                                          novi_jedan_auth_korisnik_fixture
                                                          ):
        """
        Testiranje serijalizera za pregled deatalja Korisnika koji ne postoji,
        sa fixturom od:
            * Tri kreirana nova obicna Korisnika.
            * Jednog SuperUser Korisnika.

        Testiranje se vrsi sa autorizovanim Korisnikom sistema (novi_jedan_auth_korisnik_fixture).

            * @see /test_korisnici/conftest.py (nova_tri_korisnika_fixture)
            * @see /test_korisnici/conftest.py (novi_jedan_auth_korisnik_fixture)
            * @see path('detalji-korisnika/<int:id>/', KorisniciDetaljiAPIView.as_view(), name='detalji_korisnika')

        ---
        @param client: A Django test client instance.
        @param nova_tri_korisnika_fixture: Tri obicna Korisnika
        @param novi_jedan_auth_korisnik_fixture: SuperUser Korisnik
        @return status code 404: HTTP 404 Not Found
        """

        # Get invalid one Korisnik ID from Response.
        url_detalji_korisnika = reverse('korisnici:detalji_korisnika',
                                        args=[novi_jedan_auth_korisnik_fixture.id + 1000])

        response = client.get(url_detalji_korisnika)

        assert response.status_code == 404
