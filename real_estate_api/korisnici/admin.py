from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from django.db import models

from .models import Korisnici


class UserAdminConfig(UserAdmin):
    """
    Podesavanje i promena polja i izgleda u DJANGO ADMIN sekciji.
    @see Django backend ADMIN *(Korisnici)
    """
    model = Korisnici
    search_fields = ('email', 'ime',)
    list_filter = ('id', 'email', 'is_active', 'is_staff', 'ime',)
    ordering = ('-id',)
    list_display = ('id', 'email',
                    'is_active', 'is_staff')
    fieldsets = (
        ('Osnovni Podaci', {'fields': ('email',
                                       'ime',
                                       'prezime',
                                       'username',
                                       'password',
                                       'role',
                                       'last_login',
                                       'is_superuser',
                                       )}),
        ('Permissions', {'fields': ('is_staff',
                                    'is_active'
                                    )}),

        ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'ime')}
         ),
    )


admin.site.register(Korisnici, UserAdminConfig)
