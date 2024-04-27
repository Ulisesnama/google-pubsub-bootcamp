# PubSub-Bootcamp

---

## Requisitos previos a la clase

### Instalar Docker Desktop y Configurar una Cuenta en Docker Hub

*   Descarga e instala Docker Desktop desde el [sitio web oficial de Docker](https://docs.docker.com/engine/install/).

*   Una vez instalado, crea o inicia sesión en tu cuenta de Docker Hub.

*   Abre Docker Desktop e inicia sesión con tus credenciales de Docker Hub.

### Instalar Cloud SDK Emulators y Configurar un emulador de PubSub

*   Ejecuta el siguiente comando en tu terminal para descargar la imagen Docker:
    ```
    docker pull google/cloud-sdk:emulators
    ```

*   Ejecuta el siguiente comando en tu terminal paraejecutar el contenedor Docker:
    ```
    docker run --rm -p 8085:8085 google/cloud-sdk:emulators /bin/bash -c "gcloud beta emulators pubsub start --project=testing-pubsub --host-port='0.0.0.0:8085'"
    ```
    Esto iniciará un contenedor con:
    *   El puerto expuesto en 8085 (localhost:8085) — el puerto predeterminado es el puerto 8085 para IPv6.
    *   El contenedor se basará en la imagen google/cloud-sdk:emulators.
    *   Ejecutará un comando de inicio para el emulador de Pub/Sub.
    *   El ID del proyecto es el que utilizarás más adelante, localmente, no es tu ID de proyecto real.


*   Clona el repositorio de Google PubSub
    ```
    git clone https://github.com/googleapis/python-pubsub.git
    ```

*   Navega al directorio de los snippets:
    ```
    cd python-pubsub/sample/snippets
    ```

*   Crea un ambiente virtual
    ```
    python3 -m venv env
    ```

*   Activa el ambiente virtual
  *   Activación en Unix
    ```
    source env/bin/activate
    ```
  *   Activación en Windows
    ```
    env\Scripts\activate
    ```

*   Instala los requisitos
    ```
    pip3 install -r requirements.txt
    ```

*   Exporta la variable PUBSUB_EMULATOR_HOST y PUBSUB_PROJECT_ID
    ```
    export PUBSUB_EMULATOR_HOST=localhost:8085
    export PUBSUB_PROJECT_ID=testing-pubsub
    ```
    
### Prueba que todo este correcto

*   Crea un tópico
    ```
    python publisher.py testing-pubsub create testing-topic
    ```

*   Crea una suscripción a ese topico
    ```
    python subscriber.py testing-pubsub create testing-topic testing-subscription
    ```

*   Empieza a escuchar a ese tópico
    ```
    python subscriber.py testing-pubsub receive testing-subscription
    ```
  
*   Abre otra terminal, exporta la variable PUBSUB_EMULATOR_HOST y PUBSUB_PROJECT_ID y publica al tópico
    ```
    python publisher.py testing-pubsub publish testing-topic
    ```

Si todo esta correcto, tu terminal que escucha al tópico deberia verse algo asi:
```
Listening for messages on projects/testing-pubsub/subscriptions/testing-subscription..

Received Message {
  data: b'Message number 1'
  ordering_key: ''
  attributes: {}
}.
Received Message {
  data: b'Message number 2'
  ordering_key: ''
  attributes: {}
}.
Received Message {
  data: b'Message number 3'
  ordering_key: ''
  attributes: {}
}.
Received Message {
  data: b'Message number 4'
  ordering_key: ''
  attributes: {}
}.
Received Message {
  data: b'Message number 5'
  ordering_key: ''
  attributes: {}
}.
Received Message {
  data: b'Message number 6'
  ordering_key: ''
  attributes: {}
}.
Received Message {
  data: b'Message number 7'
  ordering_key: ''
  attributes: {}
}.
Received Message {
  data: b'Message number 8'
  ordering_key: ''
  attributes: {}
}.
Received Message {
  data: b'Message number 9'
  ordering_key: ''
  attributes: {}
}.
```

## Construir un API REST con Django REST Framework

Crea un ambiente virtual:
```
python3 -m venv env
```

Activa el ambiente virtual:
```
# Activación en Unix
source env/bin/activate

# Activación en Windows
env\Scripts\activate
```

Instala Django, DRF y PyJWT:
```
pip install django
pip install djangorestframework
pip install google-cloud-pubsub
```

Crea un nuevo proyecto en Django:
```
django-admin startproject stock_alert_system
```

Crea una nueva aplicación en Django:
```
python manage.py startapp api
```

Agrega la aplicación de `rest_framework` y la que acabamos de crear en el archivo de `settings.py`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api'
]
```

Genera las migraciones y ejeculatas
```
python manage.py makemigrations
python manage.py migrate
```

Crea un super usuario
```
python manage.py createsuperuser
```

Corre la aplicación para corroborar que todo esta correcto
```
python manage.py runserver
```