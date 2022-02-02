import json

from rest_framework.reverse import reverse
from real_estate_api.lokali.lokali_api.models import Lokali


class TestLokaliSerijalizers:
    """Testiranje Serijalizers LOKALI"""

    def test_serializers_svi_lokali(self,
                                    client,
                                    nova_dva_lokala_fixture,
                                    novi_autorizovan_korisnik_fixture_lokali):
        """
        Testiranje serijalizera za pregled svih Lokala sa fixturom od dva kreirana nova Lokala.
        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_lokali)
        * @see conftest.py (nova_dva_lokala_fixture)

        @param client: A Django test client instance.
        @param nova_dva_lokala_fixture: Lokali
        @param novi_autorizovan_korisnik_fixture_lokali: Korisnik
        """

        response = client.get(reverse('lokali:lista_lokala'))

        lokali = Lokali.objects.all()
        lokali_broj = Lokali.objects.all().count()

        from real_estate_api.lokali.lokali_api.serializers import LokaliSerializer
        serializer = LokaliSerializer(lokali, many=True)

        print(f'RESPONSE DATA: {json.dumps(serializer.data)}')
        print(f'RESPONSE DATA: {json.dumps(response.json()["results"])}')

        assert json.dumps(serializer.data) == json.dumps(response.json()["results"])
        assert response.status_code == 200
        assert lokali_broj == 2

    def test_serializers_kreiraj_validan_lokal(self,
                                               client,
                                               novi_autorizovan_korisnik_fixture_lokali,
                                               novi_jedan_lokal_fixture
                                               ):
        """
        Testiranje serijalizera za kreiranje Lokala sa validnim podacima.
        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_lokali)
        """
        url_kreiraj_validan_lokal = reverse('lokali:kreiraj_lokal')

        response = client.post(url_kreiraj_validan_lokal,
                               data=novi_jedan_lokal_fixture,
                               content_type='application/json'
                               )

        assert response.status_code == 201

    def test_serializers_kreiraj_dva_lokala_sa_istim_unique_vrednostima(self,
                                                                        client,
                                                                        novi_autorizovan_korisnik_fixture_lokali,
                                                                        dva_lokala_sa_istom_lamelom_json_fixture
                                                                        ):
        """
        Testiranje serijalizera za kreiranje Lokala na istoj lameli.
        (Cime se krsi unique vrednost za to polje)
        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_lokali)
        * @see conftest.py (dva_lokala_sa_istom_lamelom_json_fixture)
        """

        url_kreiraj_lokale_na_istoj_lameli = reverse('lokali:kreiraj_lokal')

        response = client.post(
            url_kreiraj_lokale_na_istoj_lameli,
            data=dva_lokala_sa_istom_lamelom_json_fixture,
            content_type='application/json'
        )

        assert response.status_code == 400
