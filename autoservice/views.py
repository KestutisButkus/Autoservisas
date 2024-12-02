from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic

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

def car_list(request):
    cars = Automobilis.objects.all()
    context = {'cars': cars}
    # print(cars)
    return render(request, 'cars.html', context=context)

# def car_detail(request, car_id):
#     car = Automobilis.objects.get(id=car_id)
#     context = {'car': car}
#     return render(request, 'car_detail.html', context)

def car_detail(request, car_id):
    car = get_object_or_404(Automobilis, pk=car_id)
    return render(request, 'car_detail.html', {'car': car})


def cars(request):
    cars_list = Automobilis.objects.all()
    return render(request, 'cars.html', {'cars': cars_list})


class OrderListView(generic.ListView):
    model = Uzsakymas
    template_name = 'orders_list.html'
    context_object_name = 'object_list'


class OrderDetailView(generic.DetailView):
    model = Uzsakymas
    template_name = 'order_detail.html'
    context_object_name = 'details_order'  # Pakeistas kintamojo pavadinimas
