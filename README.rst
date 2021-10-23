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
