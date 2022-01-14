<table align="center">
<tr>
<td align="center" width="9999">

![STANOVI CRM](https://drive.google.com/uc?export=view&id=10PP2LghV3lHpxwj0jGEhJrPs04F9eydE)

# Customer Relationship Management: "PRODAJA STANOVA CRM" <br> ![verzija: beta v1.0](https://img.shields.io/badge/verzija-beta%20v1.0-blue)

Ovaj Repozitorijum predstavlja back-end CRM (eng. Customer Relationship Management) sistem prodaje stanova.

</td>
</tr>

<tr>
<td align="left" width="9999">

##### Developers:
- **Ivana Tepavac** (ivana.tepavac@factoryww.com)
- **Dejan Čugalj** (dejan.cugalj@factoryww.com)

</td>
</tr>
</table>

---

<table align="center">
<tr>
<td align="left" width="9999">

# Arhitektura DevOps sistema 

Arhitektura **DevOps** sistema se sastoji od:
- **BackEnd API service** servera
- Servera za **Dokument perzistenciju** (Ugovori)
- Server **Baze Podataka** (PostgreSQL 13)
- <ins>**FrontEnd** servera</ins>
</td>
</tr>
<tr>
<td align="left" width="9999">


<ins>**BackEnd API service**</ins> server:
----

Server za API servise je podignut na ["Digital Ocean App Platform"](https://try.digitalocean.com/app-platform) cloud provajderu. (**Basic Plan: $10/mo**)

```bash
App Platform provides a fully managed solution to rapidly build, deploy, manage, and scale apps.ž
Deploy code by simply pointingto GitHub or GitLab repository and let App Platform manage the infrastructure,
application runtimes, and other dependencies.
```
- GitLab 'stage' repo je povezan sa DO App platformom pa je tako i rešen CI/CD. Drugim rečima, nakon ```git push origin stage``` automatski se pokreće build na DO App platformi.
</td>
</tr>


<tr>
<td align="left" width="9999">

<ins>Servera za **Dokument perzistenciju** (Ugovori)</ins>:
----

Svaki stan potencijalno ima svoje ponude Kupaca. Ponude imaju svoje statuse i to:
- Potencijalan
- Rezervisan (kaparisan)
- Kupljen

Status ponude "rezervian" znači da je Stan kaparisan i u tom trenutku je potrebno generisati ugovor sa podacima koji se preuzimaju iz CRM sistema. Odluka koja je doneta za **perzistentno čuvanje generisanog ugovora** je:
- ["Digital Ocean Space" ](https://try.digitalocean.com/cloud-storage/) S3-compatible object storage service (**Basic Plan: $5/mo**)

</td>
</tr>


<tr>
<td align="left" width="9999">

<ins>Server **Baze Podataka** (PostgreSQL 13)</ins>:
----

Baza podataka **PostgreSQL 13**  je podignuta na:
- [Digital Ocean DataBase](https://www.digitalocean.com/products/managed-databases-postgresql/)  (**Basic Plan: $15/mo**)


</td>
</tr>

<tr>
<td align="left" width="9999">

<ins>**FrontEnd** servera</ins>:
----

- Frontend je razvijan u [REACT JavaScript library](https://reactjs.org/)
- Server je podignut na [Digital Ocean App Platform](https://docs.digitalocean.com/products/app-platform/)
- (**Basic Plan: $0/mo**)


</td>
</tr>


<tr>
<td align="left" width="9999">

<ins>Pregled DevOps Sistema</ins>:
----

slika pregled


</td>
</tr>
</table>


----


<table align="center">
<tr>
<td align="left" width="9999">

# Korišćene tehologije

Najvažnije korišćene tehologije toko razvijanja API servisa:

![Pzthon](https://img.shields.io/badge/Python-v3.9.9-blue)
![Django](https://img.shields.io/badge/Django-v3.2.8-green)
![djangorestframework](https://img.shields.io/badge/DjangoRestFramework-v3.12.4-green)
![pytest-django](https://img.shields.io/badge/PytestDjango-v4.5.2-green)
![boto3](https://img.shields.io/badge/Boto3-v1.20.27-green)
</td>
</tr>
</table>


## Kreiranje TokenAuthentication




----

- python.exe .\manage.py drf_create_token datatab

----

- U postman-u sekcija: "Authorisation" --> API Key

METHOD: Get
KEY: Authorization (For Django)
VALUE: Token 'space' API GENERATED KEY

----

Another solution :
django-rest-auth (search Google)

----

GOOD FROM DB SCHEMA online:
https://dbdiagram.io/d

----


# TESTING COMMANDS :

----

if we want to see what is the placecs that we need to test run:
1. coverage run .\manage.py test
2. coverage report
3. coverage html (to see what is to test)


SOME OTHER THINGS:
Show Coverage Data (Ctrl+Alt+F6). PyCharm

----


# DATABASE :

----

CREATE DATABASE recrm_api;


CREATE USER recrm_api WITH PASSWORD 'fwwrecrm';


ALTER ROLE recrm_api SET client_encoding TO 'utf8';
ALTER ROLE recrm_api SET default_transaction_isolation TO 'read committed';
ALTER ROLE recrm_api SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE recrm_api TO recrm_api;

# USEFUL COMMANDS:

```bash
python manage.py makemigrations --dry-run --verbosity 3
python manage.py makemigrations

python manage.py createsuperuser 

python manage.py runserver

# Print 'fixture' data from database table
python manage.py dumpdata <ime_tablele> --indent=2
# Save 'fixture' data in file
python manage.py dumpdata <ime_tablele> --indent=2 --output <putanja><ime_fajla>.json
# Load 'fixture' data file in db table 
python manage.py dumpdata <ime_tablele> --indent=2 --loaddata <putanja><ime_fajla>.json
```

