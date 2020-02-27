from django import forms
from django.forms import PasswordInput, ModelForm

from Min1.models import VOIVODESHIP_CHOICES, Category, NewsPost


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
    image = forms.ImageField(label="Zdjęcie obiektu")


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


class AddUserForm(forms.Form):
    user_name = forms.CharField(max_length=64, label='Nazwa użykownika')
    password = forms.CharField(widget=PasswordInput, label='Hasło')
    password_repeat = forms.CharField(widget=PasswordInput, label='Hasło')
    first_name = forms.CharField(max_length=64, label="Imię")
    last_name = forms.CharField(max_length=64, label="Nazwisko")
    email = forms.EmailField(max_length=64, label="E-mail")

    def clean_password_repeat(self):
        password1 = self.cleaned_data.get("password1")
        password_repeat = self.cleaned_data.get("password_repeat")
        if password1 and password_repeat and password1 != password_repeat:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password_repeat


class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(widget=PasswordInput, label="Stare hasło")
    new_password = forms.CharField(widget=PasswordInput, label="Nowe hasło")
    new_password2 = forms.CharField(widget=PasswordInput, label="Powtórz nowe hasło")

    def clean_new_password2(self):
        new_password = self.cleaned_data.get("new_password")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password and new_password2 and new_password != new_password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return new_password2


class NewsPostCreateForm(ModelForm):
    class Meta:
        model = NewsPost
        fields = ['title', 'content']
