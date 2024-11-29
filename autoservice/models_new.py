from django.db import models

class CarModel(models.Model):
    brand = models.CharField('Automobilio markė',
                             max_length=100, help_text='Įveskite markę (pvz. Volvo)')
    model = models.CharField('Automobilio modelis',
                             max_length=100, help_text='Įveskite modelį (pvz. V70)')

    def __str__(self):
        return f'{self.brand} {self.model}'

    class Meta:
        verbose_name = 'Automobilio modelis'
        verbose_name_plural = "Automobilių modeliai"

class Car(models.Model):
    car_num = models.CharField('Valstybinis NR',
                               max_length=10,
                               help_text='Įveskite valstybinį '
                                         'automobilio numerį (pvz. RRR000)')

    vin_code = models.CharField('VIN Kodas',
                                max_length=17,
                                help_text='Įveskite VIN (pvz. 2A6UR5CJXEG146621)')

    customer = models.CharField('Klientas',
                                max_length=100,
                                help_text='Vardas Pavardė (pvz. Rimas Juodaitis)')

    car_model = models.ForeignKey(CarModel,
                                  on_delete=models.CASCADE,
                                  null=False)
    # Patikrinti ar CarModel veikia ne kabutėse.

    def __str__(self):
        return f'{self.car_model} - {self.car_num} - VIN{self.vin_code} - Klientas: {self.customer}'

    class Meta:
        verbose_name = 'Automobilis'
        verbose_name_plural = "Automobiliai"

class Order(models.Model):
    date = models.DateField('Data',
                            null=True,
                            blank=True)

    car = models.ForeignKey(Car,
                            on_delete=models.CASCADE,
                            null=False)
    # Patikrinti ar Car veikia ne kabutėse.

    ORDER_STATUS = (
        ('uzregistruota', 'Užregistruota'),
        ('eileje', 'Eilėje'),
        ('tvarkoma', 'Tvarkoma'),
        ('galima_atsiimti', 'Galima atsiimti')
    )

    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS, blank=True,
        default='uzregistruota',
        help_text='Statusas',
    )

    class Meta:
        ordering = ['date']
        verbose_name = 'Užsakymas'
        verbose_name_plural = "Užsakymai"

    def __str__(self):
        return (f'Užsakymo NR. {self.id} ({self.status}, {self.date}) - '
                f'Automobilis: {self.car.car_num} VIN: {self.car.vin_code}')


class Service(models.Model):
    service_name = models.CharField('Pavadinimas',
                                    max_length=100,
                                    help_text='Įveskite paslaugos pavadinimą (pvz. Tepalų keitimas)')

    price = models.IntegerField('Kaina',
                                help_text='Įveskite paslaugos kainą (pvz. 199)')

    def __str__(self):
        return f'{self.service_name}, Kaina: {self.price}'

    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = "Paslaugos"

class OrderLine(models.Model):
    service = models.ForeignKey('Order',
                                on_delete=models.CASCADE,
                                null=False)

    order = models.ForeignKey('Service',
                              on_delete=models.CASCADE,
                              null=False)

    amount = models.IntegerField('Kiekis',
                              max_length=10,
                              help_text='Įveskite kiekį')

    def __str__(self):
        return (f'Valstybinis NR: {self.order.car.car_num} '
                f'Paslauga: {self.service.service_name} Kiekis: {self.amount}')

    class Meta:
        verbose_name = 'Užsakymo eilutė'
        verbose_name_plural = "Užsakymo eilutės"


# https://github.com/KestutisButkus/Autoservisas