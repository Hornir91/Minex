from django.forms import ModelForm

from Min1.models import Mine


class MineForm(ModelForm):
    class Meta:
        model = Mine
        fields = ['name', 'description', 'is_active', 'voivodeship', 'geom']
