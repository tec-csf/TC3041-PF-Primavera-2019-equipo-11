# TC3041 Proyecto  Final Primavera 2019

#**Mamba Fit**
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
    - backend			# Carpeta con la solución del backend (CMS)
    - api			# Carpeta con la solución de la API
    - datasets		        # Carpeta con los datasets y recursos utilizados (csv, json, audio, videos, entre otros)
    - dbs			# Carpeta con los modelos, catálogos y scripts necesarios para generar las bases de datos
    - models			# Carpeta donde se almacenarán los modelos de Machine Learning ya entrenados 
    - docs			# Carpeta con la documentación del proyecto
        - stage_f               # Documentos de la entrega final
        - manuals               # Manuales y guías
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

A continuación aparecen descritos los diferentes elementos que forman parte de la solución del proyecto.

### 3.1 Modelos de *bases de datos* utilizados

Se eligió usar MongoDB usando el servicio cloud Atlas para el manejo de la información de usuarios, clases, dietas e instructores. Y Redis usando el servicio cloud Redis Labs o un contenedor docker local para el manejo de usuarios, representados por su correo, y sus contraseñas.

La razón para usar MongoDB es que su estructura basada en documentos permite más flexibilidad para añadir información, además que el usar un servicio cloud permite tener la información respaldada.

Se usó Redis para guardar correo y contraseña, usando hash SHA-256, ya que es una base de datos de llave valor.

### 3.2 Arquitectura de la solución

Se crea un contenedor con la API y el frontend, estos se conectan con las bases de datos de manera remota, o en el caso de usar contenedores, se conectan por puertos locales.

*[Incluya aquí un diagrama donde se aprecie la arquitectura de la solución propuesta, así como la interacción entre los diferentes componentes de la misma.]*

### 3.3 Frontend

Se utilizó flask como frontend usando html.

*[Incluya aquí una explicación de la solución utilizada para el frontend del proyecto. No olvide incluir las ligas o referencias donde se puede encontrar información de los lenguajes de programación, frameworks y librerías utilizadas.]*

#### 3.3.1 Lenguaje de programación
Python
#### 3.3.2 Framework
Flask
#### 3.3.3 Librerías de funciones o dependencias
Para instalar en python, las cuales son librerias que dependen de nuestro proyecto:
pip install datetime
pip install flask
pip install flask_wtf
pip install flask_api
pip install dnspython

### 3.4 Backend

Se desarrollo en python, utilizando clases y funciones para lograr comunicar la base de datos con el front end mediante el uso de apis.

*[Incluya aquí una explicación de la solución utilizada para el backend del proyecto. No olvide incluir las ligas o referencias donde se puede encontrar información de los lenguajes de programación, frameworks y librerías utilizadas.]*

#### 3.4.1 Lenguaje de programación
python
#### 3.4.2 Framework
flask
#### 3.4.3 Librerías de funciones o dependencias

### 3.5 API

Se desarrollo en python.

*[Incluya aquí una explicación de la solución utilizada para implementar la API del proyecto. No olvide incluir las ligas o referencias donde se puede encontrar información de los lenguajes de programación, frameworks y librerías utilizadas.]*

#### 3.5.1 Lenguaje de programación
#### 3.5.2 Framework
#### 3.5.3 Librerías de funciones o dependencias

*[Incluya aquí una explicación de cada uno de los endpoints que forman parte de la API. Cada endpoint debe estar correctamente documentado.]*

*[Por cada endpoint debe incluir lo siguiente:]*

* **Descripción**:
* **URL**:
* **Verbos HTTP**:
* **Headers**:
* **Formato JSON del cuerpo de la solicitud**: 
* **Formato JSON de la respuesta**:

## 3.6 Pasos a seguir para utilizar el proyecto

* Clonar este repositorio.

* Modificar el archivo config.py para que tenga los datos correctos de base de datos. En necesario crear una cuenta en mongoDBAtlas para manejar la base de MonoDB y una cuenta en Redis Labs.

\* en caso de querer usar un contenedor local de Redis, crearlo con este comando:

     docker run --name redis-container -p 6379:6379 -d redis

* Ejecutar el archivo app.py.

* Ir a localhost:5000/login

*[Incluya aquí una guía paso a paso para poder utilizar el proyecto, desde la clonación del repositorio hasta el despliegue de la solución en una plataforma en la nube.]*

## 4. Referencias

*[Incluya aquí las referencias a sitios de interés, datasets y cualquier otra información que haya utilizado para realizar el proyecto y que le puedan ser de utilidad a otras personas que quieran usarlo como referencia]*
http://flask.pocoo.org/docs/0.12/patterns/flashing/
https://wtforms.readthedocs.io/en/stable/
http://api.mongodb.com/python/current/api/pymongo/collection.html
