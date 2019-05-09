# TC3041 Proyecto  Final Primavera 2019

# **Mamba Fit**
---

##### Integrantes:
1. Andrés Campos Tams
2. Alexandro Francisco Marcelo González


---
## 1. Aspectos generales

### 1.1 Requerimientos técnicos

A continuación se mencionan los requerimientos técnicos mínimos del proyecto, favor de tenerlos presente para que cumpla con todos.

* El equipo tiene la libertad de elegir las tecnologías de desarrollo a utilizar en el proyecto, sin embargo, debe tener presente que la solución final se deberá ejecutar en una plataforma en la nube. Puede ser  [Google Cloud Platform](https://cloud.google.com/?hl=es), [Azure](https://azure.microsoft.com/en-us/) o AWS [AWS](https://aws.amazon.com/es/free/).
* El proyecto debe utilizar al menos dos modelos de bases de datos diferentes, de los estudiados en el curso.
* La solución debe utilizar una arquitectura de microservicios. Si no tiene conocimiento sobre este tema, le recomiendo la lectura [*Microservices*](https://martinfowler.com/articles/microservices.html) de [Martin Fowler](https://martinfowler.com).
* La arquitectura debe ser modular, escalable, con redundancia y alta disponibilidad.
* La arquitectura deberá estar separada claramente por capas (*frontend*, *backend*, *API RESTful*, datos y almacenamiento).
* Los diferentes componentes del proyecto (*frontend*, *backend*, *API RESTful*, bases de datos, entre otros) deberán ejecutarse sobre contenedores [Docker](https://www.docker.com/) y utilizar [Kubernetes](https://kubernetes.io/) como orquestador.
* Todo el código, *datasets* y la documentación del proyecto debe alojarse en un repositorio de GitHub siguiendo al estructura que aparece a continuación.

### 1.2 Estructura del repositorio
El proyecto debe seguir la siguiente estructura de carpetas:
```
- / 			        # Raíz de todo el proyecto
    - README.md			# Archivo con los datos del proyecto (este archivo)
    - frontend			# Carpeta con la solución del frontend (Web app)
        -app.py
    - api			# Carpeta con la solución de la API
        -backend
    - datasets		        # Carpeta con los datasets y recursos utilizados (csv, json, audio, videos, entre otros)
    - dbs			# Carpeta con los modelos, catálogos y scripts necesarios para generar las bases de datos
```

### 1.3 Documentación  del proyecto

Como parte de la entrega final del proyecto, se debe incluir la siguiente información:

* Justificación de los modelo de *bases de datos* que seleccionaron.
* Descripción del o los *datasets* y las fuentes de información utilizadas.
* Guía de configuración, instalación y despliegue de la solución en la plataforma en la nube  seleccionada.
* Documentación de la API. Puede ver un ejemplo en [Swagger](https://swagger.io/). 
* El código debe estar documentado siguiendo los estándares definidos para el lenguaje de programación seleccionado.

## 2. Descripción del proyecto

Diseñamos una página web que simula un club deportivo local, que tiene usuarios, clases e instructores. Un administrador se encarga de dar de alta a un usuario al momento de inscripción, esta se hace de manera local, y también tiene el poder de darlo de baja. Un administrador también se encarga de añadir a los instructores contratados. Cada instructor es responsable por las clases que crea e imparte y a quien inscribe y en caso de querer eliminar una clase, tiene que ponerse en contacto con un administrador.
Los usuarios pueden consultar las clases a las que están inscritos, así como las dietas que le son recomendadas por sus instructores. Para que un usuario se inscriba a una clase, debe contactar por correo electrónico a un instructor que la imparte, de esta manera queda a discreción de cada instructor el aceptar a cada usuario a su clase, como en los casos de sobrecupo. Se fomenta la comunicación por correo para iniciar la comunicación usuario-instructor para que se aclaren los contenidos de la clase, así como el instructor pueda cuestionar al usuario sobre asuntos pertinentes a la clase (nivel, condición física, etc.). 

## 3. Solución

A continuación, aparecen descritos los diferentes elementos que forman parte de la solución del proyecto.

### 3.1 Modelos de *bases de datos* utilizados

Se eligió usar MongoDB usando el servicio cloud Atlas para el manejo de la información de usuarios, clases, dietas e instructores. Y Redis usando el servicio cloud Redis Labs para el manejo de usuarios, representados por su correo, y sus contraseñas.

La razón para usar MongoDB es que su estructura basada en documentos permite más flexibilidad para añadir información, además que el usar un servicio cloud permite tener la información respaldada.

Se usó Redis para guardar correo y contraseña, usando hash SHA-256, ya que es una base de datos de llave valor y permite la fácil recuperación de datos.

### 3.2 Arquitectura de la solución

Se crea un contenedor con la API y el frontend, estos se conectan con las bases de datos de manera remota por internet. El contenedor se encuentra en un servicio cloud con la dirección IP: 35.232.11.47.

### 3.3 Frontend

Se utilizó Flask como frontend usando html.

#### 3.3.1 Lenguaje de programación
Python
#### 3.3.2 Framework
Flask
#### 3.3.3 Librerías de funciones o dependencias
Para instalar en python, las cuales son librerias que dependen de nuestro proyecto:
pip install flask
pip install flask_wtf
pip install flask_api
pip install dnspython

### 3.4 Backend

Se desarrollo en python, utilizando clases y funciones para lograr comunicar las bases de datos con el frontend mediante el uso de una API.

#### 3.4.1 Lenguaje de programación
Python
#### 3.4.2 Framework
Flask
#### 3.4.3 Librerías de funciones o dependencias
Para instalar en python, las cuales son librerias que dependen de nuestro proyecto:
pip install flask
pip install flask_wtf
pip install flask_api
pip install dnspython

### 3.5 API

Se desarrollo en Python utilizando Flask. Cada enpoint está protegido para que únicamente quien tenga permiso de acceso pueda usarlo.

#### 3.5.1 Lenguaje de programación
Python
#### 3.5.2 Framework
Flask
#### 3.5.3 Librerías de funciones o dependencias

Para el servicio en cloud, se reemplaza *localhost:5000* por *35.232.11.47*

**Descripción**: Login para usuarios, instructores y administradores.
* **URL**: localhost:5000/ y localhost:5000/login
* **Verbos HTTP**: Get y Post
* **Headers**: Ninguno
* **Formato JSON del cuerpo de la solicitud**: {}
* **Formato JSON de la respuesta**: {}

**Descripción**: Home para todos, con sus respectivas funciones.
* **URL**: localhost:5000/home
* **Verbos HTTP**: Ninguno
* **Headers**: Ninguno
* **Formato JSON del cuerpo de la solicitud**: {}
* **Formato JSON de la respuesta**: {}

**Descripción**: Logout para usuarios, instructores y administradores.
* **URL**: localhost:5000/logout
* **Verbos HTTP**: Ninguno
* **Headers**: Ninguno
* **Formato JSON del cuerpo de la solicitud**: {}
* **Formato JSON de la respuesta**: {}

**Descripción**: Ver los datos del perfil del usuario.
* **URL**: localhost:5000/perfil
* **Verbos HTTP**: Ninguno
* **Headers**: Ninguno
* **Formato JSON del cuerpo de la solicitud**: {}
* **Formato JSON de la respuesta**: {}

**Descripción**: Ver las dietas de usuario.
* **URL**: localhost:5000/dieta
* **Verbos HTTP**: Ninguno
* **Headers**: Ninguno
* **Formato JSON del cuerpo de la solicitud**: {}
* **Formato JSON de la respuesta**: {}

**Descripción**: Borrar dietas
* **URL**: localhost:5000/delete_diet
* **Verbos HTTP**: Get y Post
* **Headers**: Ninguno
* **Formato JSON del cuerpo de la solicitud**: {}
* **Formato JSON de la respuesta**: {}

**Descripción**: Ver las clases del usuario.
* **URL**: localhost:5000/clases
* **Verbos HTTP**: Ninguno
* **Headers**: Ninguno
* **Formato JSON del cuerpo de la solicitud**: {}
* **Formato JSON de la respuesta**: {}

**Descripción**: Permite registrar usuarios.
* **URL**: localhost:5000/register_users
* **Verbos HTTP**: Get y Post
* **Headers**: Ninguno
* **Formato JSON del cuerpo de la solicitud**: {}
* **Formato JSON de la respuesta**: {}

**Descripción**: Permite eliminar usuarios.
* **URL**: localhost:5000/delete_users
* **Verbos HTTP**: Get y Post
* **Headers**: Ninguno
* **Formato JSON del cuerpo de la solicitud**: {}
* **Formato JSON de la respuesta**: {}

**Descripción**: Permite eliminar clases.
* **URL**: localhost:5000/delete_class
* **Verbos HTTP**: Get y Post
* **Headers**: Ninguno
* **Formato JSON del cuerpo de la solicitud**: {}
* **Formato JSON de la respuesta**: {}

**Descripción**: Permite registrar instructores.
* **URL**: localhost:5000/register_instructors
* **Verbos HTTP**: Get y Post
* **Headers**: Ninguno
* **Formato JSON del cuerpo de la solicitud**: {}
* **Formato JSON de la respuesta**: {}

**Descripción**: Permite crear una dieta.
* **URL**: localhost:5000/crear_dieta
* **Verbos HTTP**: Ninguno
* **Headers**: Ninguno
* **Formato JSON del cuerpo de la solicitud**: {}
* **Formato JSON de la respuesta**: {}

**Descripción**: Permite crear una clase.
* **URL**: localhost:5000/crear_clase
* **Verbos HTTP**: Ninguno
* **Headers**: Ninguno
* **Formato JSON del cuerpo de la solicitud**: {}
* **Formato JSON de la respuesta**: {}

**Descripción**: Permite añadir a un usuario a una clase.
* **URL**: localhost:5000/add_user_to_class
* **Verbos HTTP**: Ninguno
* **Headers**: Ninguno
* **Formato JSON del cuerpo de la solicitud**: {}
* **Formato JSON de la respuesta**: {}


## 3.6 Pasos a seguir para utilizar el proyecto

#Para ejecutar localmente:

* Clonar este repositorio.

* Modificar el archivo config.py para que tenga los datos correctos de base de datos. En necesario crear una cuenta en mongoDBAtlas para manejar la base de MonoDB y una cuenta en Redis Labs.

* Ejecutar el archivo app.py.

* Ir a localhost:5000/login

#Para crear el proyecto en la nube:

    Descargue el repositorio a una carpeta de su computadora utilizando el comando git clone.
    Cámbiese a la carpeta del proyecto.
    Cree un proyecto en la Consola de Google Cloud Platform. Póngale el nombre y ID que usted prefiera.
    Dentro de la misma consola, en el menú de la izquierda seleccione la opción Kubernetes Engine / Clústeres de Kubernetes y cree un nuevo clúster dentro del proyecto creado en el paso anterior.
    Cambie el nombre nombre del clúster, la versión del clúster a la 1.9.4-gke.1 y el tamaño del clúster a 1 nodo. Los demás valores déjelos como aparecen de manera predeterminada.
    Una vez creado el clúster, seleccione la opción "Ejecutar" y en la ventana que aparece, seleccione el primer comando relacionado con kubectl. El comando a copiar tiene una estructura similar a la siguiente:

gcloud container clusters get-credentials demo-webinar --zone us-central1-a --project webinar-199317

    Ejecute el comando anterior en una terminal de su computadora.
    Compile la imagen del contenedor de la aplicación, sustituyendo <PROJECT ID> por el que le correponde. Este valor es el que aparece en el parámetro --project del comando ejecutado en el paso anterior:

docker build -t gcr.io/<PROJECT ID>/flask-api app/.

    Suba la imagen del contendor al registro de su proyecto en Google Cloud Platform:

gcloud docker -- push gcr.io/<PROJECT ID>/flask-api

    Despliegue la aplicación en Google Cloud Platform:

kubectl create -f proxy-api.yaml

    Verifique que los servicios se encuentran funcionando correctamente:

kubectl get deployment kubectl get service kubectl get pod

    Obtenga la URL del servicio. Ejecute varias veces este comando hasta que el valor EXTERNAL-IP se encuentre asignado:

kubectl get service

    Acceda a la aplicación en un browser con la IP externa obtenida en el paso anterior.

    Para eliminar la aplicación y los servicios creados ejecute:

kubectl delete -f proxy-api.yaml

    Elimine el clúster desde la Consola de Google Cloud Platform.

Créditos a [vcubells](https://github.com/vcubells/kubernetes-examples/tree/master/nginx-flask-redis-mongodb)

Actualmente se puede acceder a una instancia del proyecto en cloud con la siguiente dirección: 35.232.11.47

## 4. Referencias

http://flask.pocoo.org/docs/0.12/patterns/flashing/

https://wtforms.readthedocs.io/en/stable/

http://api.mongodb.com/python/current/api/pymongo/collection.html
