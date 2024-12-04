from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound
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
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
                'num_car': num_car,
                'num_cars_bukle': num_cars_bukle,
                'num_instances_tvarkomas': num_instances_tvarkomas,
                'num_car_models': num_car_models,
                'paslaugu_kiekis': paslaugu_kiekis,
                'atlikti_uzsakymai': atlikti_uzsakymai,
                'num_visits': num_visits,
            }
    return render(request, 'index.html', context=context)

from django.core.paginator import Paginator
from django.shortcuts import render

def car_list(request):
    models_list = Automobilis.objects.all()
    paginator = Paginator(models_list, 6)
    page_number = request.GET.get('page', 1)
    car_page = paginator.get_page(page_number)
    context = {'cars': car_page}
    return render(request, 'cars.html', context=context)




def car_detail(request, car_id):
    car = get_object_or_404(Automobilis, pk=car_id)
    return render(request, 'car_detail.html', {'car': car})
    (reququest, 'cars.html', {'cars': cars_list})

class OrderListView(generic.ListView):
    model = Uzsakymas
    paginate_by = 8
    template_name = 'orders_list.html'
    context_object_name = 'object_list'

class OrderDetailView(generic.DetailView):
    model = Uzsakymas
    template_name = 'order_detail.html'
    context_object_name = 'details_order'  # Pakeistas kintamojo pavadinimas

def search(request):
    query = request.GET.get('query')
    search_results = Automobilis.objects.filter(
        Q(automobilio_modelis__modelis__icontains=query) |
        Q(klientas__icontains=query) |
        Q(valstybinis_nr__icontains=query) |
        Q(vin_kodas__icontains=query)
    )
    return render(request, 'search.html', {'cars': search_results, 'query': query})


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('index')
#     else:
#         form = UserCreationForm()
#     return render(request, 'register.html', {'form': form})
