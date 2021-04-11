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

## Interacting with the API using cURL

La API de Django nos proporciona la interfaz web, pero ¿cómo crearíamos un usuario o haríamos el login desde un cliente?
Para hacer una prueba vamos a usar cURL, una biblioteca que permite hacer peticiones en un montón de protocolos. Normalmente viene instalada en los sistemas operativos, así que sólo tenemos que abrir la terminal para empezar a probar.
Tanto el registro como el login manejan peticiones con métodos POST, podemos crearlas fácilmente.
Para registrar un usuario lo haremos así (es muy importante usar doble comillas al pasar los argumentos):

curl -X POST http://127.0.0.1:8844/api/v1/auth/registration/ -d "password1=TEST1234A&password2=TEST1234A&email=test2@test2.com"

Y para hacer login y conseguir el token:

curl -X POST http://127.0.0.1:8844/api/v1/auth/login/ -d "password=TEST1234A&email=test2@test2.com"

La idea trabajando con clientes es crear estas peticiones y almacenar el token en el localStorage del navegador para más adelante pasarlos en las cabeceras de las peticiones que requieran autenticación.

My result:

````bash
(py392_apipelis) C:\www_dj\api_pelis>curl -X POST http://127.0.0.1:8000/api/v1/auth/registration/ -d "password1=TEST1234A&password2=TEST1234A&email=test2@test2.com"
{"key":"37d54c75d630c9262c8dd95d764f16a267ee10a1"}
```
````

````bash
(py392_apipelis) C:\www_dj\api_pelis>curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ -d "password=TEST1234A&email=test2@test2.com" 
{"key":"37d54c75d630c9262c8dd95d764f16a267ee10a1"}
```
````

That´s Ok...

## Model Favorite Movie

El sistema de películas favoritas constará de dos vistas: una para marcar o desmarcar una película como favorita y otra que devolverá todas las películas favoritas del usuario.
Obviamente ambas vistas serán de acceso protegido y requerirán pasar el token de autenticación en las cabeceras. Sin embargo, antes de ponernos con las vistas tenemos que crear el nuevo modelo que relacione las películas con los usuarios en forma de favorito:

api/models.py

`from django.contrib.auth.models import User`

```
class PeliculaFavorita(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
```

Si esta relación entre una película y un usuario existe podremos entender que el usuario la tiene como favorita, y si la desmarca simplemente la borraremos de la base de datos.

Ahora vamos a añadir el serializador del modelo que utilizaremos luego:

```
class PeliculaFavoritaSerializer(serializers.ModelSerializer):

    pelicula = PeliculaSerializer()
  
    class Meta:
        model = PeliculaFavorita
        fields = ['pelicula']
```

El punto es que hacemos uso del otro serializador Pelicula dentro de PeliculaFavorita para conseguir que la API devuelva instancias anidadas, ya veréis como es muy útil.

Por ahora lo dejamos así, vamos a migrar antes de continuar con la siguiente lección:

````python
(py392_apipelis) C:\www_dj\api_pelis>python manage.py makemigrations api
Migrations for 'api':
  api\migrations\0002_auto_20210411_1404.py
    - Change Meta options on pelicula
    - Create model PeliculaFavorita

(py392_apipelis) C:\www_dj\api_pelis>python manage.py migrate api
Operations to perform:
  Apply all migrations: api
Running migrations:
  Applying api.0002_auto_20210411_1404... OK



```
````





# Comments

### wednesday, 7 april 2021 19:22

Strat Project Django Api Pelis
