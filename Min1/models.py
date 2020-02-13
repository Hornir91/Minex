from django.db import models
from django.contrib.gis.db import models as gismodels
from django.utils.text import slugify

VOIVODESHIP_CHOICES = [
    (1, "dolnośląskie"),
    (2, "kujawsko-pomorskie"),
    (3, "lubelskie"),
    (4, "lubuskie"),
    (5, "łódzkie"),
    (6, "małopolskie"),
    (7, "mazowieckie"),
    (8, "opolskie"),
    (9, "podkarpackie"),
    (10, "podlaskie"),
    (11, "pomorskie"),
    (12, "śląskie"),
    (13, "świętokrzyskie"),
    (14, "warmińsko-mazurskie"),
    (15, "wielkopolskie"),
    (16, "zachodniopomorskie")
]


class Category(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Mine(gismodels.Model):
    name = models.CharField(max_length=64, verbose_name='Nazwa')
    slug = models.SlugField(max_length=64)
    description = models.TextField(verbose_name='Opis')
    is_active = models.BooleanField(verbose_name='Czy dalej aktywna?')
    category = models.ManyToManyField(Category, verbose_name='Kategoria')
    voivodeship = models.TextField(choices=VOIVODESHIP_CHOICES, verbose_name='Województwo')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Utworzono')
    edited = models.DateTimeField(auto_now=True, verbose_name="Edytowano")
    added_by = models.CharField(max_length=64, verbose_name='Dodano przez')
    geom = gismodels.PointField(verbose_name='Dane geograficzne')
    objects = gismodels.Manager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Mine, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
