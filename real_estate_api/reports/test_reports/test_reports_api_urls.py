from dataclasses import asdict

from django.db.models import Sum
from rest_framework.reverse import reverse
from confest import novi_autorizovan_korisnik_fixture_reports, \
    novi_izvestaj_stanovi_statistika_fixture, \
    nova_tri_stana_fixture_reporti, \
    nove_tri_ponude_fixture_reporti, \
    novi_kupac_fixture_reporti, \
    novi_stan_1_fixture_stanovi, \
    novi_stan_2_fixture_stanovi, \
    novi_stan_3_fixture_stanovi, \
    azuriranje_cena_fixture, \
    novi_izvestaj_prodaja_stanova_po_agentu, \
    novi_izvestaj_prodaja_stanova_po_kupcu, \
    novi_izvestaj_roi_stanova
from real_estate_api.ponude.models import Ponude

from real_estate_api.stanovi.test_stanovi.conftest import *


class TestRestApiUrlsReports:
    """Testitanje API URLs Endpointa Reports-a"""

    def test_sa_neautorizovanim_korisnikom(self, client):
        """
        Test poziv 'endpoint_stanovi_statistika' sa neautorizovanim Korisnikom.

        * @see conftest.py (novi_neautorizovan_korisnik_fixture_reports)

        @param client: A Django test client instance.
        @return status code 401: Unauthorized
        """

        url_izvestaj_svi_stanovi = reverse('reports:reports')

        response = client.get(url_izvestaj_svi_stanovi)

        assert response.status_code == 401

    def test_sa_autorizovanim_korisnikom(self,
                                         client,
                                         novi_autorizovan_korisnik_fixture_reports,
                                         novi_jedan_stan_fixture_stanovi
                                         ):
        """
        Test poziv 'endpoint_stanovi_statistika' sa autorizovanim Korisnikom.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_reports)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_reports: Obican Korisnik sa autorizacijom.
        @return status code 200: OK
        """

        url_izvestaj_svi_stanovi = reverse('reports:reports')

        response = client.get(url_izvestaj_svi_stanovi)

        assert response.status_code == 200

    def test_kreiranje_izvestaja_za_entitet_stanovi(self, client,
                                                    nove_tri_ponude_fixture_reporti,
                                                    novi_izvestaj_stanovi_statistika_fixture,
                                                    ):
        """
        Test poziv 'endpoint_stanovi_statistika' sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_reports)
            * @see conftest.py (novi_izvestaj_stanovi_statistika_fixture)

        @param client: A Django test client instance.
        @param novi_izvestaj_stanovi_statistika_fixture: Faker.
        @param novi_autorizovan_korisnik_fixture_stanovi: Obican Korisnik sa autorizacijom.
        @return status code 200: HTTP OK
        """
        url_izvestaj_svi_stanovi = reverse('reports:reports')

        response = client.get(url_izvestaj_svi_stanovi, args=novi_izvestaj_stanovi_statistika_fixture)

        assert response.status_code == 200

        assert response.json() == {
            "ukupno_stanova": novi_izvestaj_stanovi_statistika_fixture.ukupno_stanova,
            "rezervisano": novi_izvestaj_stanovi_statistika_fixture.rezervisano,
            "dostupan": novi_izvestaj_stanovi_statistika_fixture.dostupan,
            "prodat": novi_izvestaj_stanovi_statistika_fixture.prodat,
            "procenat_rezervisan": novi_izvestaj_stanovi_statistika_fixture.procenat_rezervisan,
            "procenat_dostupan": novi_izvestaj_stanovi_statistika_fixture.procenat_dostupan,
            "procenat_prodat": novi_izvestaj_stanovi_statistika_fixture.procenat_prodat,
            "prodaja_po_mesecima": novi_izvestaj_stanovi_statistika_fixture.prodaja_po_mesecima,
            "broj_ponuda_po_mesecima": novi_izvestaj_stanovi_statistika_fixture.broj_ponuda_po_mesecima,
            "ukupna_suma_prodatih_stanova": novi_izvestaj_stanovi_statistika_fixture.ukupna_suma_prodatih_stanova
        }

    def test_prodaja_stanova_po_agentu(self, client,
                                       nove_tri_ponude_fixture_reporti,
                                       novi_izvestaj_prodaja_stanova_po_agentu
                                       ):
        url_prodaja_stanova_po_agentu = reverse('reports:reports-stanovi-po-korisniku')

        # korisnici_model =  Korisnici.objects.all()
        #
        # assert Ponude.objects.all().count() == 3
        #
        # korisnik_fixture = json.dumps(
        #     [{
        #         "id": korisnici_model[0].id,
        #         "ime": korisnici_model[0].ime,
        #         "prezime": korisnici_model[0].prezime,
        #         "email": korisnici_model[0].email,
        #         "role": korisnici_model[0].role,
        #         "prodati_stanovi_korisnici": 1
        #     }],
        # )
        #
        # test1 = dict(response.data)
        # test2 = json.dumps(korisnik_fixture).strip()
        #
        # assert test1== test2

        response = client.get(url_prodaja_stanova_po_agentu)

        assert response.status_code == 200

        # assert response.json() == {
        #     "id": novi_izvestaj_prodaja_stanova_po_agentu.id,
        #     "ime": novi_izvestaj_prodaja_stanova_po_agentu.ime,
        #     "prezime": novi_izvestaj_prodaja_stanova_po_agentu.prezime,
        #     "email": novi_izvestaj_prodaja_stanova_po_agentu.email,
        #     "role": novi_izvestaj_prodaja_stanova_po_agentu.role,
        #     "prodati_stanovi_korisnici": novi_izvestaj_prodaja_stanova_po_agentu.prodati_stanovi_korisnici
        # }

    def test_prodaja_stanova_po_kupcu(self, client,
                                      nove_tri_ponude_fixture_reporti,
                                      novi_kupac_fixture_reporti,
                                      novi_izvestaj_prodaja_stanova_po_kupcu
                                      ):
        url_prodaja_stanova_po_kupcu = reverse('reports:reports-stanovi-po-klijentu')

        response = client.get(url_prodaja_stanova_po_kupcu)

        assert response.status_code == 200

        # assert response.json() == {
        #     "id_kupca": novi_izvestaj_prodaja_stanova_po_kupcu.id_kupca,
        #     "ime_prezime": novi_izvestaj_prodaja_stanova_po_kupcu.ime_prezime,
        #     "email": novi_izvestaj_prodaja_stanova_po_kupcu.email,
        #     "prodati_stanovi_klijenti": novi_izvestaj_prodaja_stanova_po_kupcu.prodati_stanovi_klijenti,
        #     "rezervisani_stanovi_klijenti": novi_izvestaj_prodaja_stanova_po_kupcu.rezervisani_stanovi_klijenti,
        #     "potencijalan_stanovi_klijenti": novi_izvestaj_prodaja_stanova_po_kupcu.potencijalan_stanovi_klijenti
        # }

    def test_return_on_investment(self, client,
                                  novi_autorizovan_korisnik_fixture_reports,
                                  novi_stan_1_fixture_stanovi,
                                  ):
        url_return_on_investment = reverse('reports:reports-roi')

        response = client.get(url_return_on_investment)

        assert response.status_code == 200

        # assert response.json() == {
        #     "kvadratura_stanova": novi_izvestaj_roi_stanova.kvadratura_stanova,
        #     "ukupna_cena_stanova_po_lamelama": novi_izvestaj_roi_stanova.ukupna_cena_stanova_po_lamelama,
        #     "ukupan_roi_stanova": novi_izvestaj_roi_stanova.ukupan_roi_stanova
        # }
