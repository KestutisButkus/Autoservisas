from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound
from django.forms import Form
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormMixin

from .forms import OrderReviewForm
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

class OrderDetailView(FormMixin, generic.DetailView):
    model = Uzsakymas
    template_name = 'order_detail.html'
    form_class = OrderReviewForm

    # nurodome, kur atsidursime komentaro sėkmės atveju.
    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.id})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(OrderDetailView, self).form_valid(form)
    context_object_name = 'details_order'

def search(request):
    query = request.GET.get('query')
    search_results = Automobilis.objects.filter(
        Q(automobilio_modelis__modelis__icontains=query) |
        Q(klientas__icontains=query) |
        Q(valstybinis_nr__icontains=query) |
        Q(vin_kodas__icontains=query)
    )
    return render(request, 'search.html', {'cars': search_results, 'query': query})


class CarByUserView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas
    template_name = 'user_cars.html'
    paginate_by = 10

    def get_queryset(self):
        # return Uzsakymas.objects.filter(vartotojas=self.request.user).filter(status__exact='tvarkomas')
        return Uzsakymas.objects.filter(vartotojas=self.request.user)


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')