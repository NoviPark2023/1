from rest_framework.reverse import reverse
from real_estate_api.garaze.test_garaze.confest import *


class TestGarazeSerijalizers:
    """Testiranje Serijalizers GARAZE"""

    def test_serializers_sve_garaze(self,
                                    client,
                                    nove_dve_garaze_fixture,
                                    novi_autorizovan_korisnik_fixture_garaze):
        """
        Testiranje serijalizera za pregled svih Garaza sa fixturom od dve kreirane nove Garaze.
        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_garaze)
        * @see conftest.py (nove_dve_garaze_fixture)

        @param client: A Django test client instance.
        @param nove_dve_garaze_fixture: Garaze
        @param novi_autorizovan_korisnik_fixture_garaze: Korisnik
        """

        response = client.get(reverse('garaze:lista_garaza'))

        garaze = Garaze.objects.all()
        garaze_broj = Garaze.objects.all().count()

        from real_estate_api.garaze.serializers import GarazeSerializer
        serializer = GarazeSerializer(garaze, many=True)

        assert json.dumps(serializer.data) == json.dumps(response.json()["results"])
        assert response.status_code == 200
        assert garaze_broj == 2

    def test_serializers_kreiraj_validnu_garazu(self,
                                                client,
                                                novi_autorizovan_korisnik_fixture_garaze,
                                                nova_jedna_garaza_json_fixture
                                                ):
        """
        Testiranje serijalizera za kreiranje Garaze sa validnim podacima.
        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_garaze)
        """

        url_kreiraj_validnu_garazu = reverse('garaze:kreiraj_garazu')

        response = client.post(url_kreiraj_validnu_garazu,
                               data=nova_jedna_garaza_json_fixture,
                               content_type='application/json'
                               )

        assert response.status_code == 201

    def test_serializers_kreiraj_nevalidnu_garazu(self,
                                                  client,
                                                  novi_autorizovan_korisnik_fixture_garaze,
                                                  nova_jedna_nevalidna_garaza_json_fixture
                                                  ):
        """
        Testiranje serijalizera za kreiranje Garaze sa nevalidnim podacima.
        (Jedinstveni_broj_garaze ne prolazi sa negativnim integerom)
        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_garaze)
        * @see conftest.py (nova_jedna_nevalidna_garaza_json_fixture)
        """

        url_kreiraj_nevalidnu_garazu = reverse('garaze:kreiraj_garazu')

        response = client.post(url_kreiraj_nevalidnu_garazu, data=nova_jedna_nevalidna_garaza_json_fixture,
                               content_type='application/json')

        assert response.status_code == 400

    def test_serializers_kreiraj_dve_garaze_sa_istim_unique_vrednostima(
        self,
        client,
        novi_autorizovan_korisnik_fixture_garaze,
        nove_dve_garaze_sa_istim_jedinstvenim_brojem_garaze_json_fixture
        ):
        """
        Testiranje serijalizera za kreiranje Garaza sa istim jedinstvenim brojem garaze.
        (Cime se krsi unique vrednost za to polje)
        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_garaze)
        * @see conftest.py (nove_dve_garaze_sa_istim_jedinstvenim_brojem_garaze_json_fixture)
        """

        url_kreiraj_garaze_sa_istim_jedinstvenim_brojem = reverse('garaze:kreiraj_garazu')

        response = client.post(url_kreiraj_garaze_sa_istim_jedinstvenim_brojem,
                               data=nove_dve_garaze_sa_istim_jedinstvenim_brojem_garaze_json_fixture,
                               content_type='application/json')

        assert response.status_code == 400
