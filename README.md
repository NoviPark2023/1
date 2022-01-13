
<table align="center">
<tr>
<td align="center" width="9999">

![STANOVI CRM](https://drive.google.com/uc?export=view&id=10PP2LghV3lHpxwj0jGEhJrPs04F9eydE)

# Customer Relationship Management: "PRODAJA STANOVA CRM"

Ovaj Repozitorijum predstavlja back-end CRM (eng. Customer Relationship Management) sistem prodaje stanova.

</td>
</tr>
<tr>
<td align="left" width="9999">

##### Developers:
- Ivana Tepavac (ivana.tepavac@factoryww.com)
- Dejan Čugalj (dejan.cugalj@factoryww.com)



</td>
</tr>
</table>


---



</p>
</div>


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
python manage.py runserver
python manage.py createsuperuser 
pip install coverage
coverage run --omit='*/venv/*' manage.py test
coverage html
pip install djangorestframework

# Print 'fixture' data from database table
python manage.py dumpdata <ime_tablele> --indent=2
# Save 'fixture' data in file
python manage.py dumpdata <ime_tablele> --indent=2 --output <putanja><ime_fajla>.json
# Load 'fixture' data file in db table 
python manage.py dumpdata <ime_tablele> --indent=2 --loaddata <putanja><ime_fajla>.json
```

