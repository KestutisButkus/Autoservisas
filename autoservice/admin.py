from django.contrib import admin
from .models import Automobilio_modelis, Automobilis, Uzsakymas, Paslauga, Uzsakymo_eilute

class UzsakymoEiluteInline(admin.TabularInline):
    model = Uzsakymo_eilute
    extra = 2

class UzsakymasAdmin(admin.ModelAdmin):
    inlines = [UzsakymoEiluteInline]
    list_display = ("id", 'get_automobilio_modelis',
                    'terminas', 'status', "vartotojas", 'data')

    def get_automobilio_modelis(self, obj):
        return (obj.automobilis.automobilio_modelis.marke + " " +
                obj.automobilis.automobilio_modelis.modelis + " - " +
                obj.automobilis.valstybinis_nr)
    get_automobilio_modelis.short_description = 'Automobilis'

    # def get_valstybinis_nr(self, obj):
    #     return obj.automobilis.valstybinis_nr
    # get_valstybinis_nr.short_description = 'Valstybinis NR'

class AutomobilisAdmin(admin.ModelAdmin):
    list_display = ('klientas', 'automobilio_modelis', 'valstybinis_nr', 'vin_kodas')
    list_filter = ('klientas', 'automobilio_modelis')
    search_fields = ('valstybinis_nr', 'vin_kodas')
    search_help_text = 'Paieška pagal valstybinį nr., arba VIN kodą'

class PaslaugaAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'kaina', 'id')

admin.site.register(Automobilio_modelis)
admin.site.register(Automobilis, AutomobilisAdmin)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(Paslauga, PaslaugaAdmin)
admin.site.register(Uzsakymo_eilute)
