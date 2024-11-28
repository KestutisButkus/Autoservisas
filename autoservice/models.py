from django.db import models

class Automobilio_modelis(models.Model):
    marke = models.CharField('Markė', max_length=100, help_text='Įveskite markę (pvz. Ford)')
    modelis = models.CharField('Modelis', max_length=100, help_text='Įveskite modelį (pvz. Focus)')

    def __str__(self):
        return f'{self.marke} {self.modelis}'

    class Meta:
        verbose_name = 'Automobilio modelis'
        verbose_name_plural = "Automobilio modeliai"

class Automobilis(models.Model):
    valstybinis_nr = models.CharField('Valstybinis NR', max_length=15, help_text='Įveskite Valstybinį nr. (pvz. AAA000)')
    automobilio_modelis = models.ForeignKey('Automobilio_modelis', on_delete=models.CASCADE, null=False)
    vin_kodas = models.CharField('VIN Kodas', max_length=17, help_text='Įveskite VIN (pvz. 3C6UR5CJXEG146621)')
    klientas = models.CharField('Klientas', max_length=100, help_text='Vardas Pavardė (pvz. Juozas Juozaitis)')

    def __str__(self):
        return f'{self.automobilio_modelis} - {self.valstybinis_nr} - VIN{self.vin_kodas} - Klientas: {self.klientas}'

    class Meta:
        verbose_name = 'Automobilis'
        verbose_name_plural = "Automobiliai"

class Uzsakymas(models.Model):
    data = models.DateField('Data', null=True, blank=True)
    automobilis = models.ForeignKey('Automobilis', on_delete=models.CASCADE, null=False)

    LOAN_STATUS = (
        ('uzregistruotas', 'Užregistruota'),
        ('eileje', 'Eilėje'),
        ('tvarkomas', 'Tvarkoma'),
        ('galima_atsiimti', 'Galima atsiimti'),
    )

    status = models.CharField(
        max_length=20,
        choices=LOAN_STATUS,
        blank=True,
        default='uzregistruotas',
        help_text='Statusas',
    )

    class Meta:
        ordering = ['data']
        verbose_name = 'Užsakymas'
        verbose_name_plural = "Užsakymai"

    def __str__(self):
        return (f'Užsakymo NR. {self.id} ({self.status}, {self.data}) - '
                f'Automobilis: {self.automobilis.valstybinis_nr} VIN: {self.automobilis.vin_kodas}')

class Paslauga(models.Model):
    pavadinimas = models.CharField('Pavadinimas', max_length=100, help_text='Įveskite paslaugos pavadinimą (pvz. Tepalų keitimas)')
    kaina = models.IntegerField('Kaina', help_text='Įveskite paslaugos kainą (pvz. 199)')

    def __str__(self):
        return f'{self.pavadinimas}, Kaina: {self.kaina}'

    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = "Paslaugos"

class Uzsakymo_eilute(models.Model):
    paslauga = models.ForeignKey('Paslauga', on_delete=models.CASCADE, null=False)
    uzsakymas = models.ForeignKey('Uzsakymas', on_delete=models.CASCADE, null=False)
    kiekis = models.CharField('Kiekis', max_length=250, help_text='Įveskite kiekį')

    def __str__(self):
        return (f'Valstybinis NR: {self.uzsakymas.automobilis.valstybinis_nr} '
                f'Paslauga: {self.paslauga.pavadinimas} Kiekis: {self.kiekis}')

    class Meta:
        verbose_name = 'Užsakymo eilutė'
        verbose_name_plural = "Užsakymo eilutės"

"""
dėkoju https://github.com/Gvirbalis/autoservice už pavyzdinį models.py kodą
"""