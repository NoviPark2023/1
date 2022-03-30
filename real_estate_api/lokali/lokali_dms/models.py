import threading

import boto3
from django.conf import settings
from django.db import models

from real_estate_api.lokali.lokali_api.models import Lokali


class LokaliDms(models.Model):
    """ Document Managment System za entitet Lokala """
    id_fajla = models.BigAutoField(primary_key=True)
    opis_dokumenta = models.CharField(max_length=150)
    datum_ucitavanja = models.DateTimeField(auto_now_add=True)
    file = models.FileField(storage=None)

    lokal = models.ForeignKey(Lokali,
                              on_delete=models.CASCADE,
                              db_column='id_lokala',
                              related_name='lista_dokumenata_lokala'
                              )

    def __str__(self):
        return f"{self.file}"

    class Meta:
        db_table = 'lokali_dms'
        verbose_name = "Lokali Dms"
        verbose_name_plural = "Lokali Dms"
        ordering = ['-datum_ucitavanja']

    @property
    def naziv_fajla(self):
        return str(self.file)

    @property
    def lamela_lokala_dokumenti(self):
        return str(self.lokal.lamela_lokala)

    def save(self, *args, **kwargs):
        """ Ucitavanje Dokumenta Stana na DO SPACE """

        super(LokaliDms, self).save(*args, **kwargs)

        UcitajDokumentNaDoSpace(str(self.file)).start()

    def delete(self, *args, **kwargs):
        """ Brisanje Dokumenta Stana sa DO SPACE-a """

        super(LokaliDms, self).delete(*args, **kwargs)

        session = boto3.session.Session()
        client = session.client('s3',
                                region_name='fra1',
                                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                                )

        # Obrisi Dokument Stana.
        client.delete_object(
            Bucket='lokali-dms',
            Key=str(self.file)
        )


class UcitajDokumentNaDoSpace(threading.Thread):
    """Ucitaj Dokument na DO Space"""

    def __init__(self, file):
        self.file = file
        threading.Thread.__init__(self)

    def run(self):
        try:
            session_fajla_lokala = boto3.session.Session()
            client_fajla_lokala = session_fajla_lokala.client(
                's3',
                region_name='fra1',
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            # # Ucitaj na Digital Ocean Space
            client_fajla_lokala.upload_file(
                'media/' + str(self.file),
                'lokali-dms',
                self.file
            )
        except FileExistsError as e:
            print(f"Failed to send fajl: {e}")
