import boto3
from django.conf import settings
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import parsers, generics, filters
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings

from .models import StanoviDms
from .serializers import (
    StanoviDmsSerializer,
    StanoviUploadDmsSerializer
)

lookup_field = 'id_fajla'


class ListaDokumenaStanoviAPIView(generics.ListAPIView):
    """ API poziv za listu svih Dokumenata. """

    permission_classes = [IsAuthenticated]
    queryset = StanoviDms.objects.all().order_by('-datum_ucitavanja')
    serializer_class = StanoviDmsSerializer

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [
        DjangoFilterBackend,
    ]

    filterset_fields = {
        "stan": ["exact"],
    }


class StanoviDmsUploadAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = StanoviDms.objects.all()
    serializer_class = StanoviUploadDmsSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']


class ObrisiDokumentStanaAPIView(generics.DestroyAPIView):
    """ Brisanje Dokumenta Stana po 'pk-id_fajla' """
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = StanoviDms.objects.all().order_by('-datum_ucitavanja')
    serializer_class = StanoviDmsSerializer


class DokumentiStanovaDownloadAPIView(generics.ListAPIView):
    """ API View za preuzimanje dokumenata Stanova. """
    permission_classes = [IsAuthenticated, ]
    serializer_class = StanoviDmsSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):

        try:
            queryset_dokumenta = StanoviDms.objects.get(id_fajla__exact=kwargs[lookup_field])
        except StanoviDms.DoesNotExist:
            return Response({"Error": "Fajl ne postoji u sistemu."})

        try:
            session = boto3.session.Session()
            client = session.client('s3',
                                    region_name='fra1',
                                    endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

            # Generisi sigurnosni URL za preuzimanje dokumenta.
            url = client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': 'stanovi-dms',
                    'Key': str(queryset_dokumenta.file)
                }, ExpiresIn=70000
            )

        except (FileNotFoundError, StanoviDms.DoesNotExist):
            raise NotFound('Željeni dokument Stana nije nađen !', code=404)

        return HttpResponse(url)
