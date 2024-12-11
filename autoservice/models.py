from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField
from django.utils.translation import gettext_lazy as _


class Automobilio_modelis(models.Model):
    marke = models.CharField(_('Make'), max_length=100, help_text=_('Enter make (e.g., Ford)'))
    modelis = models.CharField(_('Model'), max_length=100, help_text=_('Enter model (e.g., Focus)'))
    description = HTMLField()

    def __str__(self):
        return f'{self.marke} {self.modelis}'

    class Meta:
        verbose_name = _('Car model')
        verbose_name_plural = _("Car models")


class Automobilis(models.Model):
    valstybinis_nr = models.CharField(_('License Plate'), max_length=15,
                                      help_text=_('Enter license plate (e.g., AAA000)'))
    automobilio_modelis = models.ForeignKey('Automobilio_modelis', on_delete=models.CASCADE, null=False)
    vin_kodas = models.CharField(_('VIN Code'), max_length=17, help_text=_('Enter VIN (e.g., 3C6UR5CJXEG146621)'))
    klientas = models.CharField(_('Client'), max_length=100, help_text=_('First and Last Name (e.g., John Doe)'))
    car_pic = models.ImageField(_('Photo'), upload_to='car_pic', null=True, blank=True)

    def __str__(self):
        return f'{self.automobilio_modelis} - {self.valstybinis_nr} - VIN {self.vin_kodas} - Client: {self.klientas}'

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')


class Uzsakymas(models.Model):
    data = models.DateField(_('Date'), null=True, blank=True)
    automobilis = models.ForeignKey('Automobilis', on_delete=models.CASCADE, null=False)
    vartotojas = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    terminas = models.DateField(_('Deadline'), null=True, blank=True)

    @property
    def is_overdue(self):
        if self.terminas and date.today() > self.terminas:
            return True
        return False

    LOAN_STATUS = (
        ('registered', _('Registered')),
        ('in_queue', _('In Queue')),
        ('in_repair', _('Under Repair')),
        ('ready_for_pickup', _('Ready for Pickup')),
    )

    status = models.CharField(
        max_length=20,
        choices=LOAN_STATUS,
        blank=True,
        default='registered',
        help_text=_('Status'),
    )

    class Meta:
        ordering = ['data']
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return (f'Order No. {self.id} ({self.status}, {self.data}) - '
                f'Car: {self.automobilis.valstybinis_nr} VIN: {self.automobilis.vin_kodas}')


class Paslauga(models.Model):
    pavadinimas = models.CharField(_('Service Name'), max_length=100,
                                   help_text=_('Enter service name (e.g., Oil Change)'))
    kaina = models.IntegerField(_('Price'), help_text=_('Enter service price (e.g., 199)'))

    def __str__(self):
        return f'{self.pavadinimas}, Price: {self.kaina}'

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')


class Uzsakymo_eilute(models.Model):
    paslauga = models.ForeignKey('Paslauga', on_delete=models.CASCADE, null=False)
    uzsakymas = models.ForeignKey('Uzsakymas', on_delete=models.CASCADE, null=False)
    kiekis = models.CharField(_('Quantity'), max_length=250, help_text=_('Enter quantity'))

    def __str__(self):
        return (f'License Plate: {self.uzsakymas.automobilis.valstybinis_nr} '
                f'Service: {self.paslauga.pavadinimas} Quantity: {self.kiekis}')

    class Meta:
        verbose_name = _('Order Line')
        verbose_name_plural = _('Order Lines')


class OrderReview(models.Model):
    order = models.ForeignKey('Uzsakymas', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(_('Review'), max_length=2000)

    def order_id(self):
        return self.order.id

    order_id.short_description = _('Order ID')

    def valstybinis_nr(self):
        if self.order and self.order.automobilis:
            return self.order.automobilis.valstybinis_nr
        return 'N/A'

    valstybinis_nr.short_description = _('License Plate')

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ['-date_created']


class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username}'s profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')


"""
dėkoju https://github.com/Gvirbalis/autoservice 
už pirmos paskaitos pavyzdinį models.py kodą
"""
# https://github.com/KestutisButkus/Autoservisas
