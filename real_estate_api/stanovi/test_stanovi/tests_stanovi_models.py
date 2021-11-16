from real_estate_api.korisnici.models import Korisnici
from django.test import TestCase

from ..models import Stanovi


class StanoviTestCase(TestCase):

    @classmethod
    def setUp(self):
        # Kreiraj TEST Korisnika
        self.korisnik = Korisnici.objects.create_user(
            ime='Test_Prodavac',
            prezime='Test_Prezime',
            role='Prodavac',
            username='test_user_name',
            password='test',
            email='test@example.com')

        self.broj_stanova = 5
        for i in range(0, self.broj_stanova):
            Stanovi.objects.create(
                id_stana=i,
                lamela='lamela-1',
                kvadratura=1,
                klijent_prodaje_id=self.korisnik.id
            )

    def test_queryset_exists(self):
        qs = Stanovi.objects.all()
        self.assertTrue(qs.exists())

    def test_queryset_counters(self):
        qs = Stanovi.objects.all()
        self.assertEqual(qs.count(), self.broj_stanova)

    def test_broj_stanova_korisnika_revers(self):
        # Korisnik
        korisnik = self.korisnik
        # QuerySet
        qs = korisnik.stanovi_set.all()
        print(qs)
        self.assertEqual(qs.count(), self.broj_stanova)

    def test_broj_stanova_korisnika_forwards(self):
        # Korisnik
        korisnik_id = self.korisnik.id
        # QuerySet Obj Stanovi
        qs_obj_stanovi = Stanovi.objects.filter(klijent_prodaje_id=korisnik_id)
        print(qs_obj_stanovi)
        self.assertEqual(qs_obj_stanovi.count(), self.broj_stanova)

    def test_id_korisnika_in_stanovi(self):
        # QuerySet Obj Stanovi
        korisnik_id = self.korisnik.id
        qs_obj_stanovi = Stanovi.objects.all().last()
        print(qs_obj_stanovi)
        print('-------------')
        print('Korisnik ID: ' + str(qs_obj_stanovi.klijent_prodaje_id))
        self.assertEqual(qs_obj_stanovi.klijent_prodaje_id, korisnik_id)
