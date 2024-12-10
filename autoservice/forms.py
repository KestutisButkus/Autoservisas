from django.forms import inlineformset_factory

from .models import OrderReview, Profilis, Uzsakymas, Uzsakymo_eilute
from django import forms
from django.contrib.auth.models import User


class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = OrderReview
        fields = ('content', 'order', 'reviewer',)
        widgets = {'order': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']


class DateInput(forms.DateInput):
    input_type = 'date'

class UserCarCreateForm(forms.ModelForm):
    class Meta:
        model = Uzsakymas
        fields = ['automobilis', 'vartotojas', 'terminas']
        widgets = {'vartotojas': forms.HiddenInput(), 'terminas': DateInput()}

class UzsakymoEiluteForm(forms.ModelForm):
    class Meta:
        model = Uzsakymo_eilute
        fields = ['paslauga', 'kiekis']
        widgets = {
            'kiekis': forms.TextInput(attrs={'placeholder': 'Įveskite kiekį'}),
        }
        help_texts = {
            'kiekis': None,  # Pašaliname help_text
        }

UzsakymoEiluteFormSet = inlineformset_factory(
    Uzsakymas, Uzsakymo_eilute, form=UzsakymoEiluteForm, extra=1, can_delete=True)
