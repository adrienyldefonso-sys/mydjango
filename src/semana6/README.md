# Semana 6 - Refactorización de Templates

Repositorio del proyecto:

<https://github.com/adrienyldefonso-sys/mydjango.git>

Esta carpeta contiene una copia ejecutable del proyecto preparada para los ejercicios de refactorización. Se conservaron la configuración, la base SQLite, las aplicaciones, modelos y migraciones de la Semana 5. No se modificaron modelos, migraciones ni registros del Django Admin.

## Ejecución

Desde esta carpeta:

```powershell
python manage.py runserver 127.0.0.1:8001
```

- Semana 4: `/optica-v2/`
- Semana 5: `/optica-v3/`
- Django Admin: `/admin/`

Semana 5 tiene su propio namespace (`semana5`) y sus Templates están en `semana5/templates/semana5/`, separados de los Templates de Semana 4.

## Refactorización de Semana 4

Las siete entidades trabajadas son `Cliente`, `Optometrista`, `Sucursal`, `Producto`, `HistorialClinico`, `FichaMedica` y `Venta`. Sus listados, formularios y confirmaciones ya usaban herencia de `base.html` por medio de `semana4/base_form.html` o directamente; no se crearon Views nuevas.

- En `semana4/templates/semana4/cliente_list.html` se aplicó `date:"d/m/Y"` a `cliente.fecha_nacimiento` y se añadieron comentarios Django para documentar ese formato y la sección condicional de ventas y productos de la vista de relaciones.
- El bloque común de confirmación de borrado se extrajo a `semana4/templates/semana4/partials/_confirm_delete.html` y se incluye desde `cliente_confirm_delete.html` y `optometrista_confirm_delete.html`.

## Refactorización de Semana 5

Los Templates de las siete entidades mantienen herencia desde el mismo `base.html`; los formularios heredan de `semana5/base_form.html`. Para evitar que Django resolviera los nombres duplicados de Semana 4, los Templates se separaron bajo `semana5/templates/semana5/`, sus referencias se actualizaron al namespace `semana5` y la URLconf se conectó en `/optica-v3/`.

- `semana5/templates/semana5/cliente_confirm_delete.html` y `optometrista_confirm_delete.html` reutilizan `semana5/templates/semana5/partials/_confirm_delete.html` mediante `{% include %}`.
- En `semana5/forms.py`, el alta de cliente excluye `productos`: esa relación N:M usa `Venta` como modelo intermedio y requiere fecha, cantidad, precio y estado. Los productos se asocian desde el formulario de venta. `cliente_form.html` informa este flujo.
- Las variables de Template mantienen el autoescape predeterminado de Django; no se usa el filtro `safe` en estas salidas.

## Verificación

`python manage.py check` terminó sin errores. Se comprobaron listados y formularios de ambas semanas, y se validó el flujo de alta de cliente y asociación de producto a través de una venta dentro de una transacción revertida. Las rutas públicas de Semana 5 responden bajo `/optica-v3/`; las de Semana 4 continúan bajo `/optica-v2/`.

No se añadieron paquetes nuevos, por lo que `requirements.txt` conserva sus dependencias existentes. No se realizó commit ni push como parte de esta entrega.

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

## 8. SEMANA 3 — Óptica y historial clínico

## 9. SEMANA 4 — Extensión con Ficha médica y ventas

La documentación completa del modelo ampliado, sus relaciones, consultas ORM,
CRUD del modelo intermedio y comandos de migración está disponible en
[src/semana4/README.md](src/semana4/README.md).

Repositorio para la entrega:

<https://github.com/adrienyldefonso-sys/mydjango.git>

### Auditoría del modelo de datos

| Criterio | Estado | Evidencia |
|---|---|---|
| 5 entidades de la semana 3 | ✅ | `Optometrista`, `Producto`, `Sucursal`, `Cliente`, `HistorialClinico` replcadas dentro de `semana4` |
| FK original con `related_name` y `on_delete` | ✅ | `HistorialClinico.cliente` usa `related_name='historiales'` y `CASCADE` |
| OneToOneField | ✅ | `FichaMedica.cliente` con `OneToOneField` y `related_name='ficha_medica'` |
| M2M con `through` | ✅ | `Cliente.productos` usa `through='Venta'` y `Venta` tiene `cantidad`, `precio_unitario`, `fecha_venta`, `estado` |
| Justificación por relación | ✅ | Un cliente puede tener un historial clínico, una ficha médica, y múltiples ventas por producto |
| Mínimo 7 entidades | ✅ | 5 originales + `FichaMedica` + `Venta` = 7 |
| Migraciones propias | ✅ | `semana4` crea sus tablas sin depender de `semana3` |

### Relación N:M con modelo intermedio

La relación entre `Cliente` y `Producto` está modelada con `Venta` como tabla intermedia. El flujo real es:

`Request → URL → View → Model/ORM → SQLite → View → Context → Template → Response`

En la vista se usa `Cliente.objects.prefetch_related('ventas__producto')` para obtener los clientes y, de forma optimizada, sus ventas y productos asociados, reduciendo el número de consultas. El ORM conceptual se traduce así:

- `.all()` → `SELECT *`
- `.filter()` → `SELECT ... WHERE ...`
- `select_related()` → `SELECT ... JOIN ...`
- `prefetch_related()` → múltiples `SELECT` optimizados con `IN (...)`

Este patrón evita la carga N+1 que se produciría si se consultara cada venta o producto de forma individual por cada cliente.

## 10. SEMANA 5 — Personalización del Django Admin

La investigación propia de la óptica registra las siete entidades en
`src/semana5/admin.py` mediante clases `ModelAdmin` personalizadas:

| Modelo | `list_display` | `search_fields` | `list_filter` | Relaciones expuestas |
|---|---|---|---|---|
| `Optometrista` | apellidos, nombres, número de colegiatura y teléfono | nombres, apellidos y número de colegiatura | — | — |
| `Producto` | nombre, tipo, marca, precio y stock | nombre y marca | tipo | — |
| `Sucursal` | nombre, dirección y teléfono | nombre y dirección | — | — |
| `Cliente` | apellidos, nombres, DNI, teléfono y fecha de nacimiento | nombres, apellidos y DNI | — | `FichaMedicaInline` y `VentaInline` |
| `HistorialClinico` | cliente, fecha de examen y diagnóstico | diagnóstico y datos del cliente | fecha de examen | — |
| `FichaMedica` | cliente, tipo de seguro y contacto de emergencia | datos del cliente y tipo de seguro | — | — |
| `Venta` | cliente, producto, fecha, cantidad, precio unitario y estado | datos del cliente y nombre del producto | estado y fecha de venta | — |

`FichaMedicaInline` usa `admin.StackedInline` para editar la relación
`OneToOneField` entre `Cliente` y `FichaMedica` en la misma pantalla del cliente.
`VentaInline` usa `admin.TabularInline` para editar el modelo intermedio de la
relación `ManyToManyField` entre `Cliente` y `Producto`, mostrando como columnas
editables `producto`, `fecha_venta`, `cantidad`, `precio_unitario` y `estado`.

El Admin resuelve el CRUD, las validaciones, las búsquedas, los filtros y la
edición de relaciones desde una sola pantalla. Para una interfaz dirigida al
cliente final todavía serían necesarias Views y Templates propios, con reglas
de negocio específicas, diseño visual de la óptica, permisos diferenciados por
rol y reportes personalizados.

El archivo `requirements.txt` contiene las dependencias exactas de esta entrega:
Django 5.2.17, `asgiref`, `sqlparse` y `tzdata`.


### Problemática

La óptica llevaba el registro de clientes y exámenes visuales en papel. Las fichas se perdían, se dañaban o se distribuían entre varias sucursales, lo que hacía difícil consultar el historial de un paciente, mantener el control del stock de productos y coordinar la atención de optometristas. La app `semana3` digitaliza ese flujo y centraliza la información en una base de datos relacional.

### Requisitos funcionales

1. Registrar clientes con datos personales y contacto.
2. Registrar optometristas con su número de colegiatura.
3. Registrar sucursales con dirección y teléfono.
4. Gestionar productos del catálogo con tipo, marca, precio y stock.
5. Crear un historial clínico asociado a un cliente.
6. Guardar datos refractivos como esfera, cilindro y eje por ojo.
7. Consultar todos los clientes con búsqueda por apellido o DNI.
8. Consultar todos los historiales clínicos de un cliente en orden cronológico.
9. Actualizar información sin perder trazabilidad de los registros.
10. Eliminar registros de forma segura con confirmación.
11. Mantener una estructura de datos relacional usando Django ORM.
12. Tener acceso a las entidades desde el panel de administración y a los formularios CRUD de la app.

### Entidades de la aplicación

La app `semana3` incluye estas cinco entidades principales:

- `Optometrista`: profesionales que atienden diagnósticos visuales.
- `Producto`: catálogo con armazones, lunas y lentes de contacto.
- `Sucursal`: sedes de la óptica.
- `Cliente`: pacientes registrados.
- `HistorialClinico`: información médica y refractiva asociada a cada cliente.

La relación principal es:

- `Cliente` tiene varios `HistorialClinico` mediante `ForeignKey` con `related_name='historiales'`.

### CRUD implementado

La app incluye formularios y vistas para:

- Crear registros.
- Listar registros con filtros básicos.
- Editar registros existentes.
- Eliminar con confirmación.

### URLs principales

```text
/optica/clientes/
/optica/clientes/nuevo/
/optica/clientes/<id>/editar/
/optica/clientes/<id>/eliminar/

/optica/historiales/<cliente_id>/
/optica/historiales/<cliente_id>/nuevo/
/optica/historiales/<id>/editar/
/optica/historiales/<id>/eliminar/

/optica/optometristas/
/optica/productos/
/optica/sucursales/
```

## 9. Verificaciones realizadas

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
