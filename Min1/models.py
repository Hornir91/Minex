from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.utils.text import slugify

VOIVODESHIP_CHOICES = [
    ('1', "dolnośląskie"),
    ('2', "kujawsko-pomorskie"),
    ('3', "lubelskie"),
    ('4', "lubuskie"),
    ('5', "łódzkie"),
    ('6', "małopolskie"),
    ('7', "mazowieckie"),
    ('8', "opolskie"),
    ('9', "podkarpackie"),
    ('10', "podlaskie"),
    ('11', "pomorskie"),
    ('12', "śląskie"),
    ('13', "świętokrzyskie"),
    ('14', "warmińsko-mazurskie"),
    ('15', "wielkopolskie"),
    ('16', "zachodniopomorskie"),
    ('17', "-")
]


class Category(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Comment(models.Model):
    body = models.TextField(null=True, verbose_name='Komentarz')
    user_name = models.CharField(max_length=30, verbose_name='Użytkownik')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Utworzono')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['created_on']


class Mine(gismodels.Model):
    name = models.CharField(max_length=64, verbose_name='Nazwa')
    slug = models.SlugField(max_length=64)
    description = models.TextField(verbose_name='Opis')
    is_active = models.BooleanField(verbose_name='Czy dalej aktywna?')
    category = models.ManyToManyField(Category, verbose_name='Kategoria')
    voivodeship = models.CharField(choices=VOIVODESHIP_CHOICES, max_length=30, verbose_name='Województwo')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Utworzono')
    edited = models.DateTimeField(auto_now=True, verbose_name="Edytowano")
    added_by = models.CharField(max_length=64, verbose_name='Dodano przez')
    images = models.ImageField(upload_to='media/images/', null=True)
    geom = gismodels.PointField(verbose_name='Dane geograficzne')
    objects = gismodels.Manager()
    comments = GenericRelation(Comment, verbose_name='Komentarze')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Mine, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def images_url(self):
        return self.images.url


class NewsPost(models.Model):
    title = models.CharField(max_length=50, verbose_name='Tytuł')
    content = models.TextField(verbose_name='Tekst')
    comments = GenericRelation(Comment, verbose_name="Komentarze")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Utworzono')

