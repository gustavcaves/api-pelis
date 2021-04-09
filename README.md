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
  - git remote add origin https://github.com/gustavcaves/api-pelis.git
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

# Documentation Api Pelis

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


## Install Dependencies

La autenticación con token es un sistema ideal para usar en webs asíncronas. El token es un identificador único de la sesión de un usuario que sirve como credenciales de acceso a la API. Si el cliente envía este token en sus peticiones (que generaremos cuando se registra), ésta buscará si tiene los permisos necesarios para acceder a las acciones protegidas.


Desarrollar esta funcionalidad es tedioso, pero por suerte en DRF tenemos una serie de apps que nos harán la vida mucho más fácil, sólo tenemos que configurarlas adecuadamente y en pocos minutos tendremos un sistema de autenticación básico funcionando.

pip install django-rest-auth==0.9.3
pip install django-allauth==0.38.0

apli_pelis/settings.py

`    'django.contrib.sites',`

```
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
```

```
SITE_ID = 1

ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend"
)
```

api_pelis/settings.py

```
    path('api/v1/auth/', include('rest_auth.urls')),
    path('api/v1/auth/registration/', include('rest_auth.registration.urls')),
```








# Comments

### wednesday, 7 april 2021 19:22

Strat Project Django Api Pelis
