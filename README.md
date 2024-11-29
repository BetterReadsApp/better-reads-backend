# Desarrollo y uso local

***Aclaración***: Para poder seguir los siguientes pasos, necesitás tener Docker/Docker Desktop instalado en tu máquina.

**1)** Para iniciar el contenedor de la API y el de la base de datos, ejecutar (en el root del repo):
```
./start_dev_containers
```

Si no te permite ejecutar el script anterior, ejecutar (lo mismo para cualquiera de los scripts del repo):
```
chmod +x start_dev_containers
```

**2)** Una vez que estás en la terminal del contenedor de la API, ejecutar (para hacer el setup de la DB):
```
alembic upgrade head
```

**3)** Para iniciar la API en modo local, ejecutar:
```
./start_dev
```

**4)** En tu navegador, ingresá en la siguiente URL para acceder a la documentación automática de la API:
```
localhost:8000/docs
```

***Aclaración***: Para conectarse a la API localmente desde la app utilizar ***localhost:8000*** como prefijo de todos los endpoints disponibles.
