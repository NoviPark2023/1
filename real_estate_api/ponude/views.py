from wsgiref.util import FileWrapper

from django.http import HttpResponse
from rest_framework import generics, mixins, response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from django.conf import settings
from .models import Ponude
from .serializers import PonudeSerializer
from ..stanovi.models import Stanovi

from docxtpl import DocxTemplate

lookup_field = 'id_ponude'
lookup_field_stan = 'id_stana'


class ListaPonudaAPIView(generics.ListAPIView):
    """Lista svih Ponuda"""
    permission_classes = [IsAuthenticated, ]
    queryset = Ponude.objects.all().order_by(lookup_field)
    serializer_class = PonudeSerializer


class ListaPonudaZaStanAPIView(ListaPonudaAPIView):
    """Lista svih Ponuda"""
    permission_classes = [IsAuthenticated, ]
    lookup_field_stan = lookup_field_stan
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer

    def get_queryset(self):
        """
        This view should return a list of all the Ponuda for
        the Stan as determined by the Stan ID portion of the URL.
        """
        id_stana = self.kwargs['id_stana']
        return Ponude.objects.all().filter(stan=id_stana)


class PonudeDetaljiAPIView(generics.RetrieveAPIView):
    """Get Ponude po ID-ju  || Detalji Ponude"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer


class KreirajPonudeuAPIView(generics.CreateAPIView):
    """Kreiranje nove Ponude"""
    permission_classes = [IsAuthenticated, ]
    lookup_field_stan = lookup_field_stan
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer

    def get_queryset(self):
        id_stana = self.kwargs['id_stana']
        return Ponude.objects.all().filter(stan=id_stana)



class FileDownloadListAPIView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        queryset = Ponude.objects.get(id_ponude__exact=kwargs['id_ponude'])
        file_handle = settings.MEDIA_ROOT + '/ugovor' + str(queryset.id_ponude) + '.docx'
        document = open(file_handle, 'rb')
        response = HttpResponse(FileWrapper(document), content_type='application/msword')
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_handle
        return response

class UrediPonuduViewAPI(generics.RetrieveUpdateAPIView):
    """Urednjivanje Ponude po ID-ju"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer

    def put(self, request, *args, **kwargs):
        print("REEEEEETREEEEEEEEVEEEEEEEE")

        stan = Stanovi.objects.get(id_stana__exact=request.data['stan'])
        ponuda = Ponude.objects.get(id_ponude__exact=kwargs['id_ponude'])
        ponuda_status = request.data['status_ponude']
        print(ponuda_status)
        if request.data['status_ponude'] == 'rezervisan':
            template = 'real_estate_api/static/ugovor/ugovor_tmpl.docx'
            print("TRUEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            document = DocxTemplate(template)
            context = {
                'id_stana': stan.id_stana,
                'datum_ugovora': ponuda.datum_ugovora,
                'broj_ugovora': ponuda.broj_ugovora,
                # 'kupac': ponuda.kupac,
                # 'kupac_adresa': ponuda.,
                # 'cena_stana': ponuda.cena_stana,
                # 'nacin_placanja': nacin_placanja
            }
            document.render(context)
            document.save(settings.MEDIA_ROOT + '/ugovor' + str(ponuda.id_ponude) + '.docx')
            stan.status_prodaje = 'rezervisan'
            ponuda.odobrenje = True # Potrebno odobrenje jer je stan kaparisan (Rezervisan)

        elif request.data['status_ponude'] == 'kupljen':
            # Kada Ponuda predje u status 'kupljen' automatski mapiraj polje 'prodat' u modelu Stana
            stan.status_prodaje = 'prodat'
        else:
            # Kada Ponuda predje u status 'potencijalan' automatski mapiraj polje 'dostupan' u modelu Stana
            stan.status_prodaje = 'dostupan'
            # Stan je presao u status 'Dostupa'...nije potrebno odobrenje
            ponuda.odobrenje = False

        stan.save()
        ponuda.save()

        return self.partial_update(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     """
    #     Ukoliko se cena Stana razlikuje od cene Stana u Ponudi, automatski se polje
    #     modela u Ponudama setuje na True ili False.
    #
    #     * True = Kada se cena razlikuje
    #     * False = Kada je cena ista
    #
    #     :param request: Ceo Objekat Ponue u responsu
    #     :param kwargs: Vraca ID Ponude
    #     :return: partial_update
    #     """
    #
    #     return self.partial_update(request, *args, **kwargs)
    #
    #
    # @staticmethod
    # def get_success_url():
    #     print('get_success_url')


class ObrisiPonuduAPIView(generics.RetrieveDestroyAPIView):
    """Brisanje Ponude po ID-ju"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer
