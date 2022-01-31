from rest_framework.reverse import reverse

from real_estate_api.reports.test_reports.confest import *


class TestRestApiUrlsReports:
    """Testitanje API URLs Endpointa Reports-a"""

    def test_sa_neautorizovanim_korisnikom(self, client, novi_neautorizovan_korisnik_fixture_reports):
        """
        Direktan poziv bez autorizacije endpointa:
            * 'reports:reports'
            * 'reports:reports-stanovi-po-korisniku'
            * 'reports:reports-stanovi-po-klijentu'
            * 'reports:reports-roi'

        ---
        @param client: A Django test client instance.
        @return status code 401: Unauthorized for all API endpoints.
        """

        url_izvestaj_svi_stanovi = reverse('reports:reports')
        url_reports_po_korisniku = reverse('reports:reports-stanovi-po-korisniku')
        url_reports_stanovi_po_klijentu = reverse('reports:reports-stanovi-po-klijentu')
        url_reports_roi_stanova = reverse('reports:reports-roi')

        response = client.get(url_izvestaj_svi_stanovi)
        assert response.status_code == 401

        response = client.get(url_reports_po_korisniku)
        assert response.status_code == 401

        response = client.get(url_reports_stanovi_po_klijentu)
        assert response.status_code == 401

        response = client.get(url_reports_roi_stanova)
        assert response.status_code == 401

    def test_sa_autorizovanim_korisnikom(self,
                                         client,
                                         novi_autorizovan_korisnik_fixture_reports
                                         ):
        """
        Direktan poziv sa autorizovanim Korisnikom endpointa:
            * 'reports:reports'
            * 'reports:reports-stanovi-po-korisniku'
            * 'reports:reports-stanovi-po-klijentu'

        * @see conftest.py (novi_autorizovan_korisnik_fixture_reports)

        ---
        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_reports: Obican Korisnik sa autorizacijom.
        @return status code 200: OK
        """

        url_izvestaj_svi_stanovi = reverse('reports:reports')
        url_reports_po_korisniku = reverse('reports:reports-stanovi-po-korisniku')
        url_reports_stanovi_po_klijentu = reverse('reports:reports-stanovi-po-klijentu')

        response = client.get(url_izvestaj_svi_stanovi)
        assert response.status_code == 200

        response = client.get(url_reports_po_korisniku)
        assert response.status_code == 200

        response = client.get(url_reports_stanovi_po_klijentu)
        assert response.status_code == 200

    def test_kreiranje_izvestaja_za_entitet_stanovi(self, client,
                                                    nove_tri_ponude_fixture_reporti,
                                                    novi_izvestaj_stanovi_statistika_fixture,
                                                    ):
        """
        Test poziv endpointa: 'reports:reports', sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.
        Autorizacije Korisnika se vrsi u 'nove_tri_ponude_fixture_reporti'.

            * @see  reports.test_reports.conftest.py (nove_tri_ponude_fixture_reporti)
            * @see reports.test_reports.conftest.py (novi_izvestaj_stanovi_statistika_fixture)

        ---
        @param client: A Django test client instance.
        @param novi_izvestaj_stanovi_statistika_fixture: Mock Reporta (Faker).
        @param nove_tri_ponude_fixture_reporti: Mock 3 Ponude.
        @return status code 200: HTTP OK
        """
        url_izvestaj_svi_stanovi = reverse('reports:reports')

        response = client.get(url_izvestaj_svi_stanovi, args=novi_izvestaj_stanovi_statistika_fixture)

        assert response.status_code == 200

        print('\n')
        print(f' RESPONS: {response.json()}')
        print(f' RESPONS TEST: {novi_izvestaj_stanovi_statistika_fixture.broj_ponuda_po_mesecima}')

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

    def test_prodaja_stanova_po_korisniku(self, client,
                                          nove_tri_ponude_fixture_reporti,
                                          novi_autorizovan_korisnik_fixture_reports
                                          ):
        """
        Testiranje endpointa ROI Stanova: 'reports:reports-stanovi-po-korisniku'.
        Reponse vraća sumiran broj prodatih Stanova po Korisniku(Prodavcu) sistema i
        podatke samog Korisnika.

            * @see  reports.test_reports.conftest.py (nove_tri_ponude_fixture_reporti)
            * @see reports.test_reports.conftest.py (novi_autorizovan_korisnik_fixture_reports)

        ---
        :param client: A Django test client instance.
        :param nove_tri_ponude_fixture_reporti:  Mock 3 Ponude.
        :param novi_autorizovan_korisnik_fixture_reports: Obican Korisnik sa autorizacijom.
        """
        url_prodaja_stanova_po_korisniku = reverse('reports:reports-stanovi-po-korisniku')

        # Broj autorizovanih Korisnika
        assert Korisnici.objects.all().count() == 1

        # Broj Ponuda
        assert Ponude.objects.all().count() == 3

        response = client.get(url_prodaja_stanova_po_korisniku)

        assert response.status_code == 200

        assert response.json() == \
               [
                   {
                       "id": novi_autorizovan_korisnik_fixture_reports.id,
                       "ime": novi_autorizovan_korisnik_fixture_reports.ime,
                       "prezime": novi_autorizovan_korisnik_fixture_reports.prezime,
                       "email": novi_autorizovan_korisnik_fixture_reports.email,
                       "role": novi_autorizovan_korisnik_fixture_reports.role,
                       "prodati_stanovi_korisnici": 1
                   }
               ]

    def test_prodaja_stanova_po_klijentu(self, client,
                                         nove_tri_ponude_fixture_reporti,
                                         novi_kupac_fixture_reporti,
                                         ):
        """
        Testiranje endpointa ROI Stanova: 'reports:reports-stanovi-po-klijentu'.
        Reponse vraća statistiku Stanova po Klijentu(Kupcu) i to:
            * prodati_stanovi_klijenti
            * rezervisani_stanovi_klijenti
            * potencijalan_stanovi_klijenti

        Autorizovan Korisnik se registruje u 'nove_tri_ponude_fixture_reporti' fixturi.


            * @see  reports.test_reports.conftest.py (nove_tri_ponude_fixture_reporti)
            * @see reports.test_reports.conftest.py (novi_kupac_fixture_reporti)


        ---
        :param client: A Django test client instance.
        :param nove_tri_ponude_fixture_reporti: Mock 3 Ponude.
        :param novi_kupac_fixture_reporti: Mock jednog Kupaca.
        """
        url_prodaja_stanova_po_klijentu = reverse('reports:reports-stanovi-po-klijentu')

        response = client.get(url_prodaja_stanova_po_klijentu)

        assert response.status_code == 200

        assert response.json() == \
               [
                   {
                       "id_kupca": novi_kupac_fixture_reporti.id_kupca,
                       "ime_prezime": novi_kupac_fixture_reporti.ime_prezime,
                       "email": novi_kupac_fixture_reporti.email,
                       "prodati_stanovi_klijenti": 1,
                       "rezervisani_stanovi_klijenti": 1,
                       "potencijalan_stanovi_klijenti": 1
                   }
               ]

    def test_return_on_investment(self, client,
                                  novi_autorizovan_korisnik_fixture_reports,
                                  novi_stan_1_fixture_stanovi,
                                  novi_stan_2_fixture_stanovi,
                                  novi_stan_3_fixture_stanovi,
                                  novi_izvestaj_roi_stanova,
                                  ):
        """
        Testiranje endpointa ROI Stanova: 'reports:reports-roi'.
        ROI Stanova obuhvata tri celine i to:
            * kvadratura_stanova
            * ukupna_cena_stanova_po_lamelama
            * ukupan_roi_stanova

        Sve tri celine imaju svoje sume ukupnih cena, kvadratura (sa i bez korekcija), ukupnih suma sumaraka.

        :param client: A Django test client instance.
        :param novi_autorizovan_korisnik_fixture_reports: Obican Korisnik sa autorizacijom.
        :param novi_stan_1_fixture_stanovi: Jedan entitet Stana fixture.
        :param novi_stan_2_fixture_stanovi: Jedan entitet Stana fixture.
        :param novi_stan_3_fixture_stanovi: Jedan entitet Stana fixture.
        :param novi_izvestaj_roi_stanova: Roi izvestaj Stanova
        """
        url_return_on_investment = reverse('reports:reports-roi')

        response = client.get(url_return_on_investment, args=novi_izvestaj_roi_stanova)

        assert response.status_code == 200

        print(f' FIXTURE RESPONSE: {novi_izvestaj_roi_stanova}')

        assert response.json() == {
            "kvadratura_stanova": novi_izvestaj_roi_stanova.kvadratura_stanova,
            "ukupna_cena_stanova_po_lamelama": novi_izvestaj_roi_stanova.ukupna_cena_stanova_po_lamelama,
            "ukupan_roi_stanova": novi_izvestaj_roi_stanova.ukupan_roi_stanova
        }
