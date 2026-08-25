# Proyecto Django: Sistema de Gestión de Objetos Encontrados

Aplicación web desarrollada con Django 5 para gestionar objetos encontrados en instituciones educativas. Este proyecto continúa con la app de **Semana 2** que implementa un sistema de registro y búsqueda de objetos sin base de datos.

## 📋 Problemática

En colegios, institutos y universidades, las personas suelen perder objetos dentro de las instalaciones y los avisos sobre objetos encontrados se difunden de manera desorganizada mediante grupos de WhatsApp o redes sociales. Esto dificulta que los objetos regresen a sus dueños.

## 🎯 Solución

Esta aplicación permite:
- Registrar objetos encontrados con descripción, ubicación, fecha y contacto
- Visualizar un listado completo de objetos
- Consultar detalles específicos de cada objeto
- Buscar objetos por nombre o ubicación
- Mantener los datos en memoria de forma sencilla

## 1. Tecnologías

- Python 3.14.3
- Django 5.2.17
- SQLite (para app `core`, no utilizado en `semana2`)
- HTML y plantillas de Django

Las dependencias exactas se encuentran en `requirements.txt`.

## 2. Estructura del proyecto

```text
mydjango/
|-- .venv/                         Entorno virtual local
|-- requirements.txt               Dependencias del proyecto
|-- README.md                      Este archivo
|-- src/
    |-- manage.py                  Administrador de Django
    |-- db.sqlite3                  Base de datos local (solo core)
    |-- config/
    |   |-- settings.py            Configuracion del proyecto
    |   |-- urls.py                Rutas principales
    |   |-- asgi.py                Punto de entrada ASGI
    |   `-- wsgi.py                Punto de entrada WSGI
    |-- core/                       App Semana 1 - Lista de Items
    |   |-- admin.py               Registro del modelo en Django Admin
    |   |-- models.py              Modelo Item
    |   |-- views.py               Vista item_list
    |   |-- urls.py                Rutas de la aplicacion
    |   |-- migrations/            Migraciones de base de datos
    |   `-- templates/
    |       |-- base.html           Plantilla base
    |       `-- core/item_list.html Plantilla de listado
    |
    `-- semana2/                    App Semana 2 - Objetos Encontrados
        |-- apps.py                Configuracion de la app
        |-- forms.py               Formulario ObjetoEncontradoForm
        |-- models.py              Datos en memoria (sin base de datos)
        |-- views.py               Vistas (list, detail, create)
        |-- urls.py                Rutas de la aplicacion
        |-- admin.py               (Sin uso - sin modelo de BD)
        |-- tests.py               Tests
        |-- templates/semana2/
        |   |-- objeto_list.html       Listado con búsqueda
        |   |-- objeto_detail.html     Detalles del objeto
        |   `-- objeto_create.html     Formulario de creación
        `-- README.md               Documentacion de Semana 2
```

## 3. Instalación

Desde la raíz del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

En PowerShell, si la política de ejecución lo requiere:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## 4. Ejecución

Desde `src/`, con el entorno virtual activo:

```powershell
python manage.py runserver 127.0.0.1:8000
```

Acceder en el navegador:

- **Listado de Items (core):** http://127.0.0.1:8000/
- **Objetos Encontrados (semana2):** http://127.0.0.1:8000/objetos/
- **Panel de administración:** http://127.0.0.1:8000/admin/

## 5. SEMANA 2 — Sistema de Objetos Encontrados

### Características

#### ✅ Requisito 1: Registrar objetos encontrados
- Vista de creación en `/objetos/objeto/nuevo/`
- Formulario con validaciones personalizadas
- Campos: nombre, descripción, ubicación, fecha (DD/MM/YYYY), contacto

#### ✅ Requisito 2: Visualizar objetos encontrados
- Listado en tabla en `/objetos/`
- Muestra 10 registros de ejemplo iniciales
- Información completa de cada objeto

#### ✅ Requisito 3: Consultar información de un objeto
- Vista de detalles en `/objetos/objeto/<id>/`
- Muestra todos los campos de forma legible

#### ✅ Requisito 4: Buscar objetos
- Campo de búsqueda en el listado
- Búsqueda por nombre o ubicación (case-insensitive)
- Parámetro GET: `?q=término`
- Muestra cantidad de resultados

#### ✅ Requisito 5: Registrar datos de contacto
- Campo de contacto capturado en todas las operaciones
- Se almacena junto con el objeto

### Datos iniciales (10 ejemplos)

1. Mochila negra — Biblioteca
2. Lentes de sol — Patio principal
3. Tarjeta de estudiante — Cafetería
4. Llaves — Sala de informática
5. Auriculares — Aula 305
6. Cartera de cuero marrón — Biblioteca (Segundo piso)
7. Cuaderno rojo — Aula 102
8. Teléfono móvil — Patio principal
9. Reloj de pulsera — Cafetería
10. Botella de agua — Cancha de deportes

### Importante: Datos en memoria

⚠️ **LOS DATOS SE PIERDEN AL REINICIAR EL SERVIDOR**

La app `semana2` NO utiliza base de datos. Los registros se mantienen únicamente en memoria durante la ejecución del servidor. Es un diseño intencional para esta versión inicial.

### Formulario personalizado (forms.py)

```python
class ObjetoEncontradoForm(forms.Form):
    - nombre: CharField (máx 200)
    - descripcion: CharField (mín 5 caracteres)
    - ubicacion: CharField (máx 200)
    - fecha: CharField (validación DD/MM/YYYY)
    - contacto: CharField (máx 200)
```

Todas las validaciones son personalizadas sin usar ModelForm.

### URLs de Semana 2

```
GET  /objetos/                      → objeto_list (con búsqueda)
GET  /objetos/objeto/<id>/          → objeto_detail
GET  /objetos/objeto/nuevo/         → objeto_create (formulario)
POST /objetos/objeto/nuevo/         → objeto_create (procesar)
```

### Funciones en models.py

```python
obtener_objetos()               # Retorna lista completa
obtener_objeto_por_id(id)       # Busca un objeto por ID
agregar_objeto(...)             # Agrega nuevo objeto a la lista
buscar_objetos(termino)         # Busca por nombre o ubicación
```

### Vista de creación (views.py)

La vista `objeto_create`:
- Muestra formulario en GET
- Procesa POST con validaciones
- Agrega a lista en memoria
- Redirecciona al listado

## 6. SEMANA 1 — Lista de Items (legacy)

App original que gestiona Items en base de datos (SQLite).

### Migraciones

El modelo `Item` se creó con los siguientes campos:
- `name`: texto obligatorio de hasta 200 caracteres
- `description`: texto opcional
- `created_at`: fecha y hora creada automáticamente

Para aplicar las migraciones:

```powershell
cd src
python manage.py migrate
```

### Listado principal

- URL: http://127.0.0.1:8000/
- Muestra todos los objetos `Item` de la base de datos
- Vista: `core/item_list.html`

## 7. Administración (Django Admin)

El modelo `Item` está registrado en `src/core/admin.py`. Para crear un superusuario:

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
