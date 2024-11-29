from django.http import HttpResponse
from django.shortcuts import render
from .models import Automobilio_modelis, Automobilis, Paslauga, Uzsakymas, Uzsakymo_eilute

def index(request):
    num_cars_bukle = Uzsakymas.objects.all().count()
    paslaugu_kiekis = Paslauga.objects.all().count()
    atlikti_uzsakymai = Uzsakymas.objects.filter(status__exact='galima_atsiimti').count()
    num_instances_tvarkomas = Uzsakymas.objects.filter(status__exact='tvarkomas').count()
    num_car_models = Automobilio_modelis.objects.count()
    num_car = Automobilis.objects.all().count()

    context = {
            'num_car': num_car,
            'num_cars_bukle': num_cars_bukle,
            'num_instances_tvarkomas': num_instances_tvarkomas,
            'num_car_models': num_car_models,
            'paslaugu_kiekis': paslaugu_kiekis,
            'atlikti_uzsakymai': atlikti_uzsakymai
        }
    return render(request, 'index.html', context=context)