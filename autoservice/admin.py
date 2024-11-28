from django.contrib import admin

from .models import Automobilo_modelis, Automobilis, Uzsakymas, Uzsakymo_eilute, Paslauga

admin.site.register(Uzsakymas)
admin.site.register(Automobilo_modelis)
admin.site.register(Automobilis)
admin.site.register(Uzsakymo_eilute)
admin.site.register(Paslauga)