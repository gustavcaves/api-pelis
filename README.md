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

## View Favorite Movie I


**Aclaración**

En realidad las peticiones para crear recursos sin un identificador previo son de tipo POST, mientras que las de tipo PUT se usan para crear/reemplazar las que ya existen a partir de un identificador. En otras palabras, no es no se pueda usar PUT, pero al no tener un identificador explícito es mejor utilizar POST.

**Vista**

La vista para manejar una película favorita se basa en definir un método de petición, que en nuestro caso será el PUT.

En él detectaremos una id de película que pasaremos como parámetro para recuperar la película que queremos marcar como favorita.

Una vez la tengamos recuperada crearemos la relación PeliculaFavorita, y si ya existe la borraremos haciendo lo contrario:

api/views.py

`from .models import Pelicula, PeliculaFavorita`

`from .serializers import PeliculaSerializer, PeliculaFavoritaSerializer`

```
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
```

```
class MarcarPeliculaFavorita(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # POST -> Se usa para crear un recurso sin un identificador
    # PUT -> Se usa para crear/reemplazar un recurso con un identificador
    def post(self, request):
        pelicula = get_object_or_404(Pelicula, id=self.request.data.get('id', 0))
        favorita, created = PeliculaFavorita.objects.get_or_create(pelicula=pelicula, usuario=request.user)
    # Por defecto suponemos que se crea bien
        content = {
            'id': pelicula.id,
            'favorita': True
        }
    # Si no se ha creado es que ya existe, entonces borramos el favorito
        if not created:
            favorita.delete()
            content['favorita'] = False
        return Response(content)
```

Haciendo uso de una APIView genérica configuraremos el sistema de autenticación y de permisos de la vista para que sea accesible sólo a usuarios autenticados vía token.

Ya en la respuesta devolveremos una estructura JSON usando la clase Response de DRF.

El nuevo path para acceder a la view quedará así:

api_pelis/urls.py

`    path('api/v1/favorita/', views.MarcarPeliculaFavorita.as_view()),`

Una vez configurada, si accedemos a la URL veremos como indica explícitamente la autenticación con token para tener acceso a ella.

Antes de probar si podemos añadir películas favoritas a través de cURL vamos a crear algunas películas. Normalmente añadiríamos una configuración parael adminitrador, pero ya que tenemos la interfaz de DRF nos la podemos ahorrar.

Sólo tenemos que acceder al administrador con nuestro super usuario y luego crear las películas desde la interfaz de DRF.

Para crear una petición PUT con cURL hay que estructurarla de la siguiente forma, pasando el token del usuario que marcará una película en las cabeceras:

curl -X POST http://127.0.0.1:8000/api/v1/favorita/ -H "Authorization: Token cf4d5307fe3f4b3cbd2aa403a971574e9a209c25" -d "id=1"

Se supone que si todo es correcto nos devolverá el estado de la película:

{"id":1,"favorita":true}

¿Cómo podemos saber si realmente se creó? La forma fácil sería añadir a la base de datos. Usando DB Browser for SQLite es muy fácil abrir el fichero de la base de datos y analizar los datos de las tablas.

Como hemos comprobado el registro existe, si volvemos a ejecutar la petición debería borrarla:

{"id":1,"favorita":false}


## View Favorite Movie II

Nuestra siguiente tarea es una vista que devuelva todas las películas favoritas del usuario. Por suerte gracias al serializador que creamos antes es muy fácil:

api/views.py

```
class ListarPeliculasFavoritas(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # GET -> Se usa para hacer lecturas
    def get(self, request):
        peliculas_favoritas = PeliculaFavorita.objects.filter(usuario=request.user)
        serializer = PeliculaFavoritaSerializer(peliculas_favoritas, many=True)
        return Response(serializer.data)
```

api_pelis/urls.py

`    path('api/v1/favoritas/', views.ListarPeliculasFavoritas.as_view()),`

Se trata de una simple acción de tipo GET donde devolvemos la lista de películas favoritas serializadas. Para probar si funciona haremos lo propio con cURL:

curl -X GET http://127.0.0.1:8000/api/v1/favoritas/ -H "Authorization: Token cf4d5307fe3f4b3cbd2aa403a971574e9a209c25"

Esto debería devolvernos la lista con la información de todas las películas favoritas, gracias a lo dicho anteriormente de los modelos anidados:

````python
(py392_apipelis) C:\www_dj\api_pelis>curl -X GET http://127.0.0.1:8000/api/v1/favoritas/ -H "Authorization: Token cf4d5307fe3f4b3cbd2aa403a971574e9a209c25"    
[{"pelicula":{"id":1,"titulo":"Iron Man","estreno":2008,"imagen":"https://m.media-amazon.com/images/M/MV5BMTczNTI2ODUwOF5BMl5BanBnXkFtZTcwMTU0NTIzMw@@._V1_UX182_CR0,0,182,268_AL_.jpg","resumen":"After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight 
evil."}}]
```
````








# Comments

### wednesday, 7 april 2021 19:22

Strat Project Django Api Pelis
