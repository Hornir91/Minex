from django import forms
from django.forms import PasswordInput

from Min1.models import VOIVODESHIP_CHOICES, Category


class MineForm(forms.Form):
    name = forms.CharField(max_length=64, label='Nazwa')
    description = forms.CharField(widget=forms.Textarea, label='Opis')
    is_active = forms.TypedChoiceField(coerce=lambda x: x == 'True',
                                       choices=((False, 'Nie'), (True, 'Tak')), label="Czy dalej aktywna?")
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), label='Kategoria')
    voivodeship = forms.ChoiceField(choices=VOIVODESHIP_CHOICES, label='Województwo')
    added_by = forms.CharField(max_length=64, label='Dodano przez')
    lat = forms.FloatField(label="Szerokość geograficzna")
    lng = forms.FloatField(label='Długość geograficzna')


# class MineEditForm(forms.Form):
#     name = forms.CharField(max_length=64, label='Nazwa')
#     description = forms.Textarea()
#     is_active = forms.BooleanField(label='Czy dalej aktywna?')
#     category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), label='Kategoria')
#     voivodeship = forms.ChoiceField(choices=VOIVODESHIP_CHOICES, label='Województwo')
#     added_by = forms.CharField(max_length=64, label='Dodano przez')
#     lng = forms.FloatField(label='Długość geograficzna')
#     lat = forms.FloatField(label="Szerokość geograficzna")


class LoginForm(forms.Form):
    login = forms.CharField(min_length=3, max_length=32)
    password = forms.CharField(widget=PasswordInput)
