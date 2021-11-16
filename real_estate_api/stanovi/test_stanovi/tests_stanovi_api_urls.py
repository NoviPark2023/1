from django.test import TestCase
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from ..models import Stanovi


class TestStanoviAppModels(TestCase):
    """Testing Stanovi Models __str__ and __repr__"""


    @classmethod
    def setUpClass(self):
        super(TestStanoviAppModels, self).setUpClass()
        self.number_of_stanova = 5
        self.stanovi = []
        for i in range(0, self.number_of_stanova):
            self.stanovi.append(Stanovi.objects.create(id_stana=i, lamela="dea_"+str(i), kvadratura=15))
    ##############################################################
    # GOOOOOOOOOOOOOOOOOODDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
    ##############################################################



    def test_model_repr(self):
        for i in range(1, 5):
            self.assertEqual(str(self.stanovi), str(i)+', dea_'+str(i)+',  15')
            #self.assertEqual(str(self.stanovi.id_stana), '1')
            #self.assertEqual(str(self.stanovi.lamela), 'dea')
            #self.assertEqual(str(self.stanovi.kvadratura), '15')

    def test_detalji_stana_API_end_point(self):
        # response = self.stanovi.po.reverse('detalji-stana/', kwargs={'id_stana':1})
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = Stanovi.objects.all().last()
        print(obj.pk)
        print(obj.lamela)
        print('------------------')
        #print(self.stanovi.lamela)


class URLTest(APITestCase, URLPatternsTestCase):
    """Testing RECRM APIs"""

    urlpatterns = [
        path('', include('real_estate_api.stanovi.urls')),
    ]

    def test_lista_stanova_API_end_point(self):
        """Test lista stanova API end point"""
        url = reverse('')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
