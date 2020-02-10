from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from Min1.models import Mine


class BaseView(View):

    def get(self, request):
        return render(request, 'base.html')





class MineCreate(View):

    def get(self, request):
        form = MineForm()
        return render(request, 'mine_create.html', locals())

    def post(self, request):
        form = MineForm(request.POST)
        if form.is_valid():
            return
