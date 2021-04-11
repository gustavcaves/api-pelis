from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Pelicula(models.Model):
    titulo = models.CharField(max_length=150)
    estreno = models.IntegerField(default=2000)
    imagen = models.URLField(help_text="De imdb mismo")
    resumen = models.TextField(help_text="Descripción corta")
    class Meta:
        ordering = ['titulo']

class PeliculaFavorita(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)