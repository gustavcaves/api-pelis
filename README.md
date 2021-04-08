# Web Api Pelis

In this repositoy I will be getting the documentation of the proyect web playgorund, class base view

# How to upload this repository

[Index](#Index)

- Creo el repo en github normal si novedad, en blanco.
- Creo el README.md con la estructura de documentacion como puedes ver.
- **Y luego aplico estos comandos:**

  - git init
  - git add .
  - git commit -m "first commit"
  - git branch -M main
  - git remote add origin https://github.com/gustavcaves/web_playground_project.git
  - git push -u origin main
- **Luego para seguir actualizando:**

  - git status
  - **git add .**
  - git status
  - **git commit -m "another commit"**
  - git status
  - **git push -u origin main**

# Create Virtual Environment With Conda

[Index](#Index)

- conda create -n py392_apipelis python
- activate : $ conda activate py392_apipelis
- deactivate : $ conda deactivate

# Start a Project in Django

- django-admin startproject api_pelis

# Password Login

admin | 1234

# Link de Post

# Requirements

pip freeze > requirements.txt

Original Requirements:

* [X] django==2.2.3
* [X] djangorestframework==3.9.1
* [X] markdown==3.0.1
* [X] django-filter==2.1.0

# Documentation Web Playground

## Creating The Project

installed app in settings 'rest_framework'

django-admin startproject api_pelis

python manage.py startapp api

python manage.py migrate

python manage.py createsuperuser

## Movie Model and Serializer

api/models.py

```
class Pelicula(models.Model):
    titulo = models.CharField(max_length=150)
    estreno = models.IntegerField(default=2000)
    imagen = models.URLField(help_text="De imdb mismo")
    resumen = models.TextField(help_text="Descripción corta")
class Meta:
    ordering = ['titulo']
```

api/serializer.py

```
from .models import Pelicula
from rest_framework import serializers

class PeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        # fields = ['id', 'titulo', 'imagen', 'estreno', 'resumen']
        fields = '__all__'
```

## ViewSet and Url

api/views.py

```
from .models import Pelicula
from .serializers import PeliculaSerializer
from rest_framework import viewsets

class PeliculaViewSet(viewsets.ModelViewSet):
    queryset = Pelicula.objects.all()
    serializer_class = PeliculaSerializer
```

api_pelis/urls.py

```
from django.contrib import admin
from django.urls import path, include

from api import views
from rest_framework import routers
router = routers.DefaultRouter()

# En el router vamos añadiendo los endpoints a los viewsets
router.register('peliculas', views.PeliculaViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('admin/', admin.site.urls),
]
```

api_pelis/settings.py

```
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
 ],
}
```




















# Comments

### wednesday, 7 april 2021 19:22

Strat Project Django Api Pelis
