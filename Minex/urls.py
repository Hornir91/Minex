"""Minex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, re_path, include
from django.views.generic import RedirectView
from djgeojson.views import GeoJSONLayerView

from Min1.models import Mine
from Min1.views import Dashboard, MineCreate, MineEdit, MineList, MapDisplay, MineDetails, Login, Logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Dashboard.as_view(), name='dashboard'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico'))),
    path('mine_create/', MineCreate.as_view(), name='mine-create'),
    re_path(r'^mine_edit/(?P<id>\d+)/$', MineEdit.as_view(), name='mine-edit'),
    path('mine_list/', MineList.as_view(), name='mine-list'),
    path('map_display', MapDisplay.as_view(), name='map-display'),
    url(r'^data.geojson$', GeoJSONLayerView.as_view(model=Mine), name='data'),
    re_path(r'^mine_details/(?P<id>\d+)/$', MineDetails.as_view(), name='mine-details'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
