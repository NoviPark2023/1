from rest_framework.reverse import reverse


class TestRestApiUrlsReportsGaraze:
    """Testitanje API URLs Endpointa Reports-a Garaza"""

    def test_sa_neautorizovanim_korisnikom(self, client, novi_neautorizovan_korisnik_fixture_reports_garaze):
        """
        Direktan poziv bez autorizacije endpointa:
            * 'reports-garaze:reports-garaze'
        ---
        @param client: A Django test client instance.
        @return status code 401: Unauthorized for all API endpoints.
        """

        url_izvestaj_sve_garaze = reverse('reports-garaze:reports-garaze')

        response = client.get(url_izvestaj_sve_garaze)
        assert response.status_code == 401

    def test_sa_autorizovanim_korisnikom(self,
                                         client,
                                         novi_autorizovan_korisnik_fixture_reports_garaze
                                         ):
        """
        Direktan poziv sa autorizovanim Korisnikom endpointa:
            * 'reports-garaze:reports-garaze'

        * @see conftest.py (novi_autorizovan_korisnik_fixture_reports_garaze)
        ---
        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_reports_garaze: Obican Korisnik sa autorizacijom.
        @return status code 200: OK
        """

        url_izvestaj_sve_garaze = reverse('reports-garaze:reports-garaze')

        response = client.get(url_izvestaj_sve_garaze)
        assert response.status_code == 200

    def test_kreiranje_izvestaja_za_entitet_garaze(self, client,
                                                   nove_tri_garaze_fixture,
                                                   novi_izvestaj_garaze_statistika_fixture,
                                                   novi_autorizovan_korisnik_fixture_reports_garaze
                                                   ):
        """
        Test poziv endpointa: 'reports-garaze:reports-garaze', sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see  reports.test_reports_garaze.conftest.py (nove_tri_garaze_fixture)
            * @see reports.test_reports_garaze.conftest.py (novi_izvestaj_garaze_statistika_fixture)
            * @see reports.test_reports_garaze.conftest.py (novi_autorizovan_korisnik_fixture_reports_garaze)

        ---
        @param client: A Django test client instance.
        @param novi_izvestaj_garaze_statistika_fixture: Mock Reporta Garaza (Faker).
        @param nove_tri_garaze_fixture: Mock 3 Ponude.
        @return status code 200: HTTP OK
        """
        url_izvestaj_sve_garaze = reverse('reports-garaze:reports-garaze')

        response = client.get(url_izvestaj_sve_garaze, args=novi_izvestaj_garaze_statistika_fixture)

        assert response.status_code == 200

        print('\n')
        print(f' RESPONS: {response.json()}')
        print(f' RESPONS TEST: {novi_izvestaj_garaze_statistika_fixture.broj_ponuda_za_garaze_po_mesecima}')

        assert response.json() == {
            "ukupno_garaza": novi_izvestaj_garaze_statistika_fixture.ukupno_garaza,
            "rezervisano_garaza": novi_izvestaj_garaze_statistika_fixture.rezervisano_garaza,
            "dostupno_garaza": novi_izvestaj_garaze_statistika_fixture.dostupno_garaza,
            "prodato_garaza": novi_izvestaj_garaze_statistika_fixture.prodato_garaza,
            "procenat_rezervisanih_garaza": novi_izvestaj_garaze_statistika_fixture.procenat_rezervisanih_garaza,
            "procenat_dostupnih_garaza": novi_izvestaj_garaze_statistika_fixture.procenat_dostupnih_garaza,
            "procenat_prodatih_garaza": novi_izvestaj_garaze_statistika_fixture.procenat_prodatih_garaza,
            "prodaja_garaza_po_mesecima": novi_izvestaj_garaze_statistika_fixture.prodaja_garaza_po_mesecima,
            "broj_ponuda_za_garaze_po_mesecima": novi_izvestaj_garaze_statistika_fixture.broj_ponuda_za_garaze_po_mesecima,
            "ukupna_suma_prodatih_garaza": novi_izvestaj_garaze_statistika_fixture.ukupna_suma_prodatih_garaza
        }
