from django.contrib.gis.geos import Point
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View


from Min1.forms import MineForm, MineEditForm
from Min1.models import Mine


class Dashboard(View):

    def get(self, request):
        return render(request, 'dashboard.html')





class MineCreate(View):

    def get(self, request):
        form = MineForm()
        return render(request, 'mine_create.html', locals())

    def post(self, request):
        form = MineForm(request.POST)

        if form.is_valid():
            lng = form.cleaned_data.get('lng')
            lat = form.cleaned_data.get('lat')
            m1 = Mine.objects.create(name=form.cleaned_data.get('name'), description=form.cleaned_data.get('description'),
                                     is_active=form.cleaned_data.get('is_active'), voivodeship=form.cleaned_data.get('voivodeship'),
                                     added_by=form.cleaned_data.get('added_by'), geom=Point(lng, lat))
            return redirect(reverse_lazy('dashboard'))


class MineEdit(View):

    def get(self, request, id):
        mine = Mine.objects.get(pk=id)
        form = MineEditForm()
        return render(request, 'mine_edit.html', {'form': form})

    def post(self, request, id):
        form = MineEditForm(request.POST, initial=[Mine.objects.get(pk=id)])
        if form.is_valid():
            m1 = Mine.objects.get(pk=id)
            lng = form.cleaned_data.get('lng')
            lat = form.cleaned_data.get('lat')
            m1.name = form.cleaned_data.get('name')
            m1.description = form.cleaned_data.get('description')
            m1.is_active = form.cleaned_data.get('is_active')
            m1.voivodeship = form.cleaned_data.get('voivodeship')
            m1.added_by = form.cleaned_data.get('added_by')
            m1.geom = Point(lng, lat)
            m1.save()
        return redirect((reverse_lazy('dashboard')))

