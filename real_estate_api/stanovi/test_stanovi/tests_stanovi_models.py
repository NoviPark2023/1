from real_estate_api.korisnici.models import Korisnici
from django.test import TestCase

from ..models import Stanovi


class StanoviTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Kreiraj TEST Korisnika
        cls.korisnik = Korisnici.objects.create(
            ime='Test_Prodavac',
            prezime='Test_Prezime',
            role='Prodavac',
            username='test_user_name',
            password='test',
            email='test@example.com')

        cls.broj_stanova = 5
        for i in range(0, cls.broj_stanova):
            Stanovi.objects.create(
                id_stana=i,
                lamela='lamela-1',
                kvadratura=1,
                klijent_prodaje_id=cls.korisnik.id
            )

    def test_queryset_exists(self):
        qs = Stanovi.objects.all()
        print('QUERY: ' + str(qs))
        self.assertTrue(qs.exists())

    def test_queryset_counters(self):
        qs = Stanovi.objects.all()
        print('QUERY-Koliko ima stanova: ' + str(qs.count()))
        self.assertEqual(qs.count(), self.broj_stanova)

    def test_broj_stanova_korisnika_revers(self):
        # Korisnik
        korisnik = self.korisnik
        # QuerySet
        qs = korisnik.stanovi_set.all()
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

    def test_str_from_stanovi_models(self):
        qs = Stanovi.objects.get(id_stana=1)
        print(f'QUERI STAN >>  {qs}')
        print(f'QUERI STANA ID:1 >>  {qs.id_stana}')
        print(f'QUERI STANA ID:1 >>  {qs.lamela}')
        self.assertEqual(str(qs), qs.__str__())
