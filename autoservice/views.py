from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound
from django.forms import Form
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin, CreateView, UpdateView, DeleteView
from .forms import OrderReviewForm, UserUpdateForm, ProfilisUpdateForm, UserCarCreateForm, UzsakymoEiluteFormSet
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uzsakymo_eilutes = self.object.uzsakymo_eilute_set.all()
        bendra_suma = 0
        for eilute in uzsakymo_eilutes:
            eilute.bendra_kaina = eilute.paslauga.kaina * int(eilute.kiekis)
            bendra_suma += eilute.bendra_kaina
        context['uzsakymo_eilutes'] = uzsakymo_eilutes
        context['bendra_suma'] = bendra_suma
        return context

    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

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

@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profilis.html', context)


class CarByUserDetailView(LoginRequiredMixin, DetailView):
    model = Uzsakymas
    template_name = 'user_car.html'


class CarByUserCreateView(LoginRequiredMixin, CreateView):
    model = Uzsakymas
    success_url = "/autoservice/mycars/"
    template_name = 'user_car_form.html'
    form_class = UserCarCreateForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['eilutes'] = UzsakymoEiluteFormSet(self.request.POST)
        else:
            data['eilutes'] = UzsakymoEiluteFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        eilutes = context['eilutes']
        form.instance.vartotojas = self.request.user  # Priskiriame vartotoją
        form.instance.data = timezone.now().date()  # Nustatome šiandienos datą
        self.object = form.save()

        if eilutes.is_valid():
            eilutes.instance = self.object
            eilutes.save()

        return super().form_valid(form)



class CarByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Uzsakymas
    fields = ['automobilis', 'terminas']
    success_url = "/autoservice/mycars/"
    template_name = 'user_car_form.html'

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        return super().form_valid(form)

    def test_func(self):
        car = self.get_object()
        return self.request.user == car.vartotojas

class CarByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Uzsakymas
    success_url = "/autoservice/mycars/"
    template_name = 'user_car_delete.html'

    def test_func(self):
        car = self.get_object()
        return self.request.user == car.vartotojas
