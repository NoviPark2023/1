from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Stanovi
from .serializers import StanoviSerializer, ListaPonudaStanaSerializer

lookup_field = 'id_stana'


class ListaStanovaAPIView(generics.ListAPIView):
    """Lista svih Stanova"""
    permission_classes = [IsAuthenticated, ]
    queryset = Stanovi.objects.all().order_by('id_stana')
    serializer_class = StanoviSerializer


class StanoviDetaljiAPIVIew(generics.RetrieveAPIView):
    """Get Stanovi po ID-ju || DETALJI STANA"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Stanovi.objects.all()
    serializer_class = StanoviSerializer


class KreirajStanAPIView(generics.CreateAPIView):
    """Kreiranje novog Stana"""
    permission_classes = [IsAuthenticated, ]
    queryset = Stanovi.objects.all()
    serializer_class = StanoviSerializer

    def post(self, request, *args, **kwargs):
        """
        Prilikom kreiranja Stana automatski update polja 'klijent_prodaje, sa
        korisnikom koji je prijavljen.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # TODO: ivana.tepavac implement [PS-64]
        #  @hint *(Dobijanje prijavljenog korisnika iz requesta-)
        print('test post funkcije prilikom CREATE stana')
        return self.create(request, *args, **kwargs)


class UrediStanViewAPI(generics.RetrieveUpdateAPIView):
    """EDIT Stana poi polju 'id_stana '"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Stanovi.objects.all()
    serializer_class = StanoviSerializer


class ObrisiStanViewAPI(generics.RetrieveDestroyAPIView):
    """Brisanje Stana"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Stanovi.objects.all()
    serializer_class = StanoviSerializer


class ListaPonudaStanaAPIView(generics.RetrieveAPIView):
    """Lista svih Ponuda Stana"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Stanovi.objects.all().order_by('id_stana')
    serializer_class = ListaPonudaStanaSerializer

    def get_queryset(self):
        id_stana = self.kwargs['id_stana']
        return Stanovi.objects.all().filter(stan=id_stana)
