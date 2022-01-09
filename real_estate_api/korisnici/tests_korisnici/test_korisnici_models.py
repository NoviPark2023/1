from real_estate_api.korisnici.models import Korisnici


class TestEntitetaKorisnici:
    """Testitanje entiteta Korisnici"""

    def test_kreiranje_jednog_novog_korisnika(self, novi_jedan_auth_korisnik_fixture):
        """
        Testiranje kreiranja novog jednog Korisnika i provera podataka nakon kreiranja.
            * @see /test_korisnici/conftest.py : novi_jedan_auth_korisnik_fixture

        @param novi_jedan_auth_korisnik_fixture: entitet Korisnici
        """

        korisnik_from_db = Korisnici.objects.all()
        email = korisnik_from_db[0].email
        username = korisnik_from_db[0].username
        password = korisnik_from_db[0].password
        ime = korisnik_from_db[0].ime
        prezime = korisnik_from_db[0].prezime
        role = korisnik_from_db[0].role
        about = korisnik_from_db[0].about
        is_staff = korisnik_from_db[0].is_staff
        is_active = korisnik_from_db[0].is_active
        is_superuser = korisnik_from_db[0].is_superuser

        assert novi_jedan_auth_korisnik_fixture.email == email
        assert novi_jedan_auth_korisnik_fixture.username == username
        assert novi_jedan_auth_korisnik_fixture.password == password
        assert novi_jedan_auth_korisnik_fixture.ime == ime
        assert novi_jedan_auth_korisnik_fixture.prezime == prezime
        assert novi_jedan_auth_korisnik_fixture.role == role
        assert novi_jedan_auth_korisnik_fixture.about == about
        assert novi_jedan_auth_korisnik_fixture.is_staff == is_staff
        assert novi_jedan_auth_korisnik_fixture.is_active == is_active
        assert novi_jedan_auth_korisnik_fixture.is_superuser == is_superuser

    def test_broj_novih_korisnika_u_bazi(self, novi_jedan_auth_korisnik_fixture):
        """
        Test da li je samo jedan korisnik kreiran u bazi.
            * @see /test_korisnici/conftest.py : novi_jedan_auth_korisnik_fixture

        @param novi_jedan_auth_korisnik_fixture: Korisnici
        """

        broj_korisnika_u_bazi = Korisnici.objects.all().count()
        assert broj_korisnika_u_bazi == 1

    def test_kreiranje_tri_nova_korisnika(self, nova_tri_korisnika_fixture):
        """
        Testiranje kreiranja nova tri Korisnika i provera podataka nakon kreiranja.
            * @see /test_korisnici/conftest.py : nova_tri_korisnika_fixture

        @param nova_tri_korisnika_fixture: entitet Korisnici
        """
        korisnici = Korisnici.objects.all().values()
        print(f'KORISNIK IZ DBa: {korisnici}')

        broj_korisnika_u_bazi = Korisnici.objects.all().count()

        # Ovde je 4 jer u bazi pored ova tri ima i jedn registrovan super-user Korisnik.
        assert broj_korisnika_u_bazi == 4


# class PasswordChange(TestCase):
#     def test_change_password(self):
#         c = Client()
#         url = 'http://0.0.0.0:8000/korisnici/izmeni-korisnika/14/'
#         payload = {'csrf_token': csrf_token, 'payload': json.dumps({'password': 'test2'})}
#         headers = {'Cookie': 'csrftoken=' + csrf_token}
#
#         res = c.post(url, payload, headers=headers)
#         res = res.json()
#         self.assertEqual(res['password_changed'], True)
#         korisnik = Korisnici.objects.get(username='ivana')
#         self.assertEqual(korisnik.check_password('test2'), True)
