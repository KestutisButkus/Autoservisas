from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField


class Automobilio_modelis(models.Model):
    marke = models.CharField('Markė', max_length=100, help_text='Įveskite markę (pvz. Ford)')
    modelis = models.CharField('Modelis', max_length=100, help_text='Įveskite modelį (pvz. Focus)')
    description = HTMLField()

    def __str__(self):
        return f'{self.marke} {self.modelis}'

    class Meta:
        verbose_name = 'Automobilio modelis'
        verbose_name_plural = "Automobilio modeliai"


class Automobilis(models.Model):
    valstybinis_nr = models.CharField('Valstybinis NR', max_length=15,
                                      help_text='Įveskite Valstybinį nr. (pvz. AAA000)')
    automobilio_modelis = models.ForeignKey('Automobilio_modelis', on_delete=models.CASCADE, null=False)
    vin_kodas = models.CharField('VIN Kodas', max_length=17, help_text='Įveskite VIN (pvz. 3C6UR5CJXEG146621)')
    klientas = models.CharField('Klientas', max_length=100, help_text='Vardas Pavardė (pvz. Juozas Juozaitis)')
    car_pic = models.ImageField('Foto', upload_to='car_pic', null=True, blank=True)

    def __str__(self):
        return f'{self.automobilio_modelis} - {self.valstybinis_nr} - VIN{self.vin_kodas} - Klientas: {self.klientas}'

    class Meta:
        verbose_name = 'Automobilis'
        verbose_name_plural = "Automobiliai"


class Uzsakymas(models.Model):
    data = models.DateField('Data', null=True, blank=True)
    automobilis = models.ForeignKey('Automobilis', on_delete=models.CASCADE, null=False)
    vartotojas = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    terminas = models.DateField('Terminas', null=True, blank=True)

    @property
    def is_overdue(self):
        if self.terminas and date.today() > self.terminas:
            return True
        return False

    LOAN_STATUS = (
        ('uzregistruotas', 'Užregistruota'),
        ('eileje', 'Eilėje'),
        ('tvarkomas', 'Vyksta reomonto darbai'),
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
    pavadinimas = models.CharField('Pavadinimas', max_length=100,
                                   help_text='Įveskite paslaugos pavadinimą (pvz. Tepalų keitimas)')
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


class OrderReview(models.Model):
    order = models.ForeignKey('Uzsakymas', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Atsiliepimas', max_length=2000)

    def order_id(self):
        return self.order.id

    order_id.short_description = 'Order ID'

    def valstybinis_nr(self):
        if self.order and self.order.automobilis:
            return self.order.automobilis.valstybinis_nr
        return 'N/A'

    valstybinis_nr.short_description = 'Valstybinis NR'

    class Meta:
        verbose_name = "Atsiliepimas"
        verbose_name_plural = 'Atsiliepimai'
        ordering = ['-date_created']

class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)

    class Meta:
        verbose_name = "Profilis"
        verbose_name_plural = 'Profiliai'


"""
dėkoju https://github.com/Gvirbalis/autoservice 
už pirmos paskaitos pavyzdinį models.py kodą
"""
# https://github.com/KestutisButkus/Autoservisas
