from django.conf import settings
from docxtpl import DocxTemplate

from real_estate_api.kupci.models import Kupci
from real_estate_api.ponude.models import Ponude
from real_estate_api.stanovi.models import Stanovi


class CreateContract:

    @staticmethod
    def create_contract(request, **kwargs):
        """
        * U trenutku setovanja statusa ponuda na 'Rezervisan', Stan se smatra kaparisan.
        * Potrebno je odobrenje vlasnika-administratora sistema ove ponude @see(ponuda.odobrenje = True).
        * Takodje se setuje status Stana na 'rezervisan', @see(stan.status_prodaje = 'rezervisan')
        :param request: Ponude
        """

        stan = Stanovi.objects.get(id_stana__exact=request.data['stan'])
        ponuda = Ponude.objects.get(id_ponude__exact=kwargs['id_ponude'])
        kupac = Kupci.objects.get(id_kupca__exact=request.data['kupac'])

        if request.data['status_ponude'] == 'rezervisan':
            template = 'real_estate_api/static/ugovor/ugovor_tmpl.docx'
            document = DocxTemplate(template)
            context = {
                'id_stana': stan.id_stana,
                'datum_ugovora': ponuda.datum_ugovora.strftime("%d.%m.%Y."),
                'broj_ugovora': ponuda.broj_ugovora,
                'kupac': kupac.ime_prezime,
                'adresa_kupaca': kupac.adresa,
                'kvadratura': stan.kvadratura,
                'cena_stana': ponuda.cena_stana_za_kupca,
                # 'nacin_placanja': nacin_placanja
            }
            document.render(context)
            document.save(settings.MEDIA_ROOT + '/ugovor' + str(ponuda.id_ponude) + '.docx')
            stan.status_prodaje = 'rezervisan'

            ponuda.odobrenje = True  # Potrebno odobrenje jer je stan kaparisan (Rezervisan)

            stan.save()
            ponuda.save()

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
