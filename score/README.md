# Proyecto grupo 13

Proyecto orientado a optimizar la utilización del espacio disponible en las maletas de los viajeros con el fin de facilitar el envío de paquetes. Los arrendatarios tienen la posibilidad de ofrecer parte del espacio de sus maletas a cambio de una compensación económica, mientras que los arrendadores pueden alquilar dicho espacio para enviar sus paquetes. La infraestructura del proyecto se compone de cuatro microservicios diseñados para gestionar trayectos, publicaciones, ofertas y usuarios, proporcionando así una experiencia integral y segura para los participantes.

## Índice

1. [Estructura](#estructura)
2. [Ejecución](#ejecución)
3. [Uso](#uso)
4. [Pruebas](#pruebas)
5. [Otras caracteristicas](#Otras Características (opcional))
6. [Autor](#autor)

## Estructura

Describe la estructura de archivos de la carpeta, puedes usar una estructura de arbol para ello:

``
│   └── src # contiene el código y la lógica necesarios para declarar y ejecutar la API del microservicio
│   	└── blueprints carpeta contiene la capa de aplicación de nuestro microservicio
│   	└── commands carpeta contiene cada caso de uso que estamos implementando
│   	└── errors carpeta para devolver errores HTTP en los blueprints
│   	└── models carpeta contiene la capa de persistencia
│   └── tests # Esta carpeta contiene las pruebas para los componentes principales del microservicio
│   	└── blueprints pruebas unitarias de los blueprints
│   	└── commands pruebas unitarias de los comandos
│   └── .env.template # Archivo de plantilla Env utilizado para definir variables de entorno
│   └── .env.test # Archivo utilizado para definir variables de entorno para las pruebas unitarias
│   └── Dockerfile # Definición para construir la imagen Docker del microservicio
│   └── Pipfile # Este archivo declara todas las dependencias que serán utilizadas por el microservicio
│   └── README.md # usted esta aquí
``

## Ejecución

Instalar dependencias
```
$> pipenv shell
$> pipenv install
```

Variables de entorno

DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=score_db
USERS_PATH=api_user

Ejecutar el servicio

```
# Routes
$> FLASK_APP=./src/main.py flask run -h 0.0.0.0 -p 3002

```

## Uso

Ejecutar pruebas con postman

Para probar los servicios API expuestos por cada microservicio, hemos proporcionado una lista de colecciones de Postman que puedes ejecutar localmente descargando cada archivo JSON de colección e importándolo en Postman.

Lista de colecciones de Postman para cada entrega del proyecto:

Entrega 1: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-monitor/main/entrega1/entrega1.json


## Pruebas

Para ejecutar pruebas unitarias
```
pytest --cov-fail-under=70 --cov=src
pytest --cov-fail-under=70 --cov=src --cov-report=html
```

## Otras Características (opcional)

Nuestro proyecto no tiene caracteristicas adicionales.

## Autor

Monica Muñoz Beltran
Humberto Maury Maury
Fredy Alarcon Fonseca
Jhon Bohorquez Guerrero