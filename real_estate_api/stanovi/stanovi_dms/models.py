import threading

import boto3
from django.conf import settings
from django.db import models

from real_estate_api.stanovi.models import Stanovi


class StanoviDms(models.Model):
    """ Document Managment System za entitet Stanova """
    id_fajla = models.BigAutoField(primary_key=True)
    opis_dokumenta = models.CharField(max_length=150)
    datum_ucitavanja = models.DateTimeField(auto_now_add=True)
    file = models.FileField(storage=None)

    stan = models.ForeignKey(Stanovi,
                             on_delete=models.CASCADE,
                             db_column='id_stana',
                             related_name='lista_dokumenata_stana'
                             )

    def __str__(self):
        return f"{self.file}"

    class Meta:
        db_table = 'stanovi_dms'
        verbose_name = "Stanovi Dms"
        verbose_name_plural = "Stanovi Dms"
        ordering = ['-datum_ucitavanja']

    @property
    def naziv_fajla(self):
        return str(self.file)

    @property
    def lamela_stana_dokumenti(self):
        return str(self.stan.lamela)

    def save(self, *args, **kwargs):
        """ Ucitavanje Dokumenta Stana na DO SPACE """

        super(StanoviDms, self).save(*args, **kwargs)

        UcitajDokumentNaDoSpace(str(self.file)).start()

    def delete(self, *args, **kwargs):
        """ Brisanje Dokumenta Stana sa DO SPACE-a """

        super(StanoviDms, self).delete(*args, **kwargs)

        session = boto3.session.Session()
        client = session.client('s3',
                                region_name='fra1',
                                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                                )

        # Obrisi Dokument Stana.
        client.delete_object(
            Bucket='stanovi-dms',
            Key=str(self.file)
        )


class UcitajDokumentNaDoSpace(threading.Thread):
    """Ucitaj Dokument na DO Space"""

    def __init__(self, file):
        self.file = file
        threading.Thread.__init__(self)

    def run(self):
        try:
            session_fajla_stana = boto3.session.Session()
            client_fajla_stana = session_fajla_stana.client(
                's3',
                region_name='fra1',
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            # # Ucitaj na Digital Ocean Space
            client_fajla_stana.upload_file(
                'media/' + str(self.file),
                'stanovi-dms',
                self.file
            )
        except FileExistsError as e:
            print(f"Failed to send fajl: {e}")
