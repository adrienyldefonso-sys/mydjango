# Proyecto Django: Lista de Items

Aplicacion web desarrollada con Django 5 para gestionar y mostrar una lista de items. Este documento resume los ejercicios realizados y explica como instalar, ejecutar y verificar el proyecto.

## 1. Tecnologias

- Python 3.14.3
- Django 5.2.17
- SQLite
- HTML y plantillas de Django

Las dependencias exactas se encuentran en `requirements.txt`.

## 2. Estructura del proyecto

```text
mydjango/
|-- .venv/                         Entorno virtual local
|-- requirements.txt               Dependencias del proyecto
|-- README.md                      Documentacion
|-- src/
    |-- manage.py                  Administrador de Django
    |-- db.sqlite3                  Base de datos local
    |-- config/
    |   |-- settings.py            Configuracion del proyecto
    |   |-- urls.py                Rutas principales
    |   |-- asgi.py                Punto de entrada ASGI
    |   `-- wsgi.py                Punto de entrada WSGI
    `-- core/
        |-- admin.py               Registro del modelo en Django Admin
        |-- models.py              Modelo Item
        |-- views.py               Vista item_list
        |-- urls.py                Rutas de la aplicacion
        |-- migrations/            Migraciones de base de datos
        `-- templates/
            |-- base.html           Plantilla base
            `-- core/item_list.html Plantilla de listado
```

## 3. Instalacion

Desde la raiz del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

En PowerShell, si la politica de ejecucion lo requiere, se puede activar el entorno para la sesion actual con:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## 4. Migraciones

El modelo `Item` se creo con los siguientes campos:

- `name`: texto obligatorio de hasta 200 caracteres.
- `description`: texto opcional.
- `created_at`: fecha y hora creada automaticamente.

Para aplicar las migraciones:

```powershell
cd src
python manage.py makemigrations
python manage.py migrate
```

## 5. Ejecucion

Desde `src/`, con el entorno virtual activo:

```powershell
python manage.py runserver 127.0.0.1:8000
```

Abrir en el navegador:

- Listado principal: http://127.0.0.1:8000/
- Panel de administracion: http://127.0.0.1:8000/admin/

## 6. Datos de prueba

Se crearon dos registros para verificar el listado:

1. **Primer item**: Elemento de prueba número uno.
2. **Segundo item**: Elemento de prueba número dos.

La pagina principal consulta todos los objetos `Item` mediante `Item.objects.all()` y los muestra con la plantilla `core/item_list.html`. Si no existen registros, se muestra el mensaje de estado vacio mediante `{% empty %}`.

## 7. Administracion

El modelo `Item` esta registrado en `src/core/admin.py`. Para crear otro superusuario:

```powershell
cd src
python manage.py createsuperuser
```

El superusuario creado durante el desarrollo puede acceder a `/admin/` con sus credenciales.

## 8. Verificaciones realizadas

- `python manage.py check`: sin errores.
- `python manage.py makemigrations`: genero `core/migrations/0001_initial.py`.
- `python manage.py migrate`: migraciones aplicadas correctamente.
- `GET /`: respuesta HTTP 200.
- La pagina principal mostro los dos items de prueba.
- `GET /admin/`: redireccion al login HTTP 302 cuando no hay una sesion autenticada.
- `requirements.txt`: generado con las dependencias instaladas.

## 9. Publicacion en GitHub

El proyecto debe publicarse desde la raiz `mydjango`, no desde `.venv` ni desde `src`:

```powershell
git init
git add .
git commit -m "Crear proyecto Django de lista de items"
git branch -M main
git remote add origin https://github.com/USUARIO/REPOSITORIO.git
git push -u origin main
```

Sustituye `USUARIO/REPOSITORIO` por el repositorio real de GitHub. No se deben incluir contraseñas ni secretos en el repositorio.
