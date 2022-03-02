# API Curadeuda


A continuación se muestran los pasos para poder correr la aplicación y verificar su funcionamiento.

Se hizo uso de flask para la construcción de APIs y MySQL para almacenar los datos

## Comandos para correr la aplicación
Para poder hacer uso de la aplicación se debe tener docker y docker compose instalado,
de lo contrario no funcionará.
```sh
cd examen
docker-compose up
docker exec -it app_sepomex python extract.py
```
Este último comando es para llenar la base de datos con datos que contiene el archivo de excel. Este proceso puede tardar un poco
ya que se hace migración de todos los datos.

##Rutas
Para poder consumir la API se hicieron la creación de las siguientes rutas:
```sh
127.0.0.1/states
127.0.0.1/municipalities
127.0.0.1/colonies - (contiene paginación de 10)
127.0.0.1/colonies/<cp> - en lugar de "cp" poner cualquier codigo postal.
``
