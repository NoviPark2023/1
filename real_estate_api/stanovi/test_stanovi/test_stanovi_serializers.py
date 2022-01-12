import json
from decimal import Decimal

from rest_framework.reverse import reverse

from real_estate_api.stanovi.models import Stanovi


class TestStanovicSerijalizers:
    """Testiranje Serijalizers STANOVI"""

    def test_serializers_svi_stanovi(self,
                                     client,
                                     nova_dva_stana_fixture,
                                     novi_autorizovan_korisnik_fixture_stanovi):
        """
        Testiranje serijalizera za pregled svih Stanova sa fixturom od dva kreirana nova Stana.
        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)
        * @see conftest.py (nova_dva_stana_fixture)

        @param client: A Django test client instance.
        @param nova_dva_stana_fixture: Stanovi
        @param novi_autorizovan_korisnik_fixture_stanovi: Korisnik
        """

        response = client.get(reverse('stanovi:lista_stanova'))

        stanovi = Stanovi.objects.all()
        stanovi_broj = Stanovi.objects.all().count()

        from real_estate_api.stanovi.serializers import StanoviSerializer
        serializer = StanoviSerializer(stanovi, many=True)

        print(f'RESPONSE DATA: {json.dumps(serializer.data)}')
        print(f'RESPONSE DATA: {json.dumps(response.json()["results"])}')

        assert json.dumps(serializer.data) == json.dumps(response.json()["results"])
        assert response.status_code == 200
        assert stanovi_broj == 2

    def test_serializers_kreiraj_validan_stan(self,
                                              client,
                                              novi_autorizovan_korisnik_fixture_stanovi,
                                              kreiraj_auriranje_cena,
                                              novi_jedan_stan_fixture
                                              ):
        """
        Testiranje serijalizera za kreiranje Stana sa validnim podacima.
        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)
        * @see conftest.py (kreiraj_auriranje_cena)
        """

        url_kreiraj_validan_stan = reverse('stanovi:kreiraj_stan')

        # validan_stan = json.dumps(
        #     {'id_stana':3,
        #      'lamela':"L4.1.S2",
        #      'adresa_stana':"Adresa Stana L3.1.S2",
        #      'kvadratura':'48.02',
        #      'kvadratura_korekcija':46.58,
        #      'iznos_za_korekciju_kvadrature':'0.97',
        #      'sprat':"1.0",
        #      'broj_soba':2,
        #      'orijentisanost':"Jug",
        #      'broj_terasa':0,
        #      'cena_stana':"73036.50",
        #      'cena_kvadrata':"1568.00",
        #      'napomena':'Nema napomene',
        #      'status_prodaje':"dostupan"}
        # )

        response = client.post(url_kreiraj_validan_stan, data=novi_jedan_stan_fixture, content_type='application/json')

        assert response.status_code == 201

    def test_serializers_kreiraj_nevalidan_stan(self,
                                                client,
                                                novi_autorizovan_korisnik_fixture_stanovi,
                                                kreiraj_auriranje_cena,
                                                novi_jedan_nevalidan_stan_json_fixture
                                                ):
        """
        Testiranje serijalizera za kreiranje Stana sa nevalidnim podacima.
        (Broj_terasa ne prolazi sa negativnim integerom,
        ni sprat ne prolazi kao integer, jer se ne nalazi poklapanje za azuriranje cena)
        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)
        * @see conftest.py (kreiraj_auriranje_cena)
        * @see conftest.py (novi_jedan_nevalidan_stan_json_fixture)
        """

        url_kreiraj_nevalidan_stan = reverse('stanovi:kreiraj_stan')

        response = client.post(url_kreiraj_nevalidan_stan, data=novi_jedan_nevalidan_stan_json_fixture,
                               content_type='application/json')

        assert response.status_code == 400

    def test_serializers_kreiraj_dva_stana_sa_istim_unique_vrednostima(self,
                                                                       client,
                                                                       novi_autorizovan_korisnik_fixture_stanovi,
                                                                       kreiraj_auriranje_cena,
                                                                       nova_dva_stana_sa_istom_lamelom_json_fixture
                                                                       ):
        """
        Testiranje serijalizera za kreiranje Stanova na istoj lameli.
        (Cime se krsi unique vrednost za to polje)
        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)
        * @see conftest.py (kreiraj_auriranje_cena)
        * @see conftest.py (nova_dva_stana_sa_istom_lamelom_json_fixture)
        """

        url_kreiraj_stan_na_istoj_lameli = reverse('stanovi:kreiraj_stan')

        response = client.post(url_kreiraj_stan_na_istoj_lameli, data=nova_dva_stana_sa_istom_lamelom_json_fixture,
                               content_type='application/json')

        assert response.status_code == 400


    def test_invalid_serializers_detalji_jednog_stana(self,
                                                      client,
                                                      nova_dva_stana_fixture,
                                                      novi_autorizovan_korisnik_fixture_stanovi
                                                      ):
        """
        Testiranje serijalizera za pregled deatalja Stana koji ne postoji
        sa fixturom od dva kreirana nova Stana.

        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)
        * @see conftest.py (nova_dva_stana_fixture)

        @param client: A Django test client instance.
        @param nova_dva_stana_fixture: Stanovi
        @param novi_autorizovan_korisnik_fixture_stanovi: Korisnik
        """

        # Get invalid one Kupaca from Response
        url_detalji_stana_jedan = reverse('stanovi:detalji_stana', args=[nova_dva_stana_fixture[0].id_stana + 1000])
        response = client.get(url_detalji_stana_jedan)
        assert response.status_code == 404
