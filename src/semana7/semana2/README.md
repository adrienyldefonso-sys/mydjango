# Semana 2 — Sistema de Objetos Encontrados

## Descripción general

Esta aplicación permite registrar objetos perdidos dentro de una institución educativa y consultarlos posteriormente. La idea central es que una persona pueda reportar un objeto encontrado con sus datos básicos de contacto, la ubicación exacta o aproximada en la que fue hallado, la fecha y una breve descripción para identificarlo.

La versión actual ya no trabaja con datos temporales en memoria, sino con una base de datos real usando Django ORM y SQLite. Esto hace que los registros se conserven entre reinicios del servidor.

---

## Qué se ha implementado

### 1. Modelo principal `ObjetoEncontrado`
Se creó el modelo real que representa cada objeto reportado. Tiene los siguientes campos:
- `nombre`: nombre del objeto
- `descripcion`: detalle del objeto
- `ubicacion`: relación con la entidad `Ubicacion`
- `fecha`: fecha en que fue encontrado
- `contacto`: datos de contacto de quien lo reportó

Este modelo se define en `models.py` y se usa con el ORM de Django para guardar, consultar y actualizar registros.

### 2. Modelo complementario `Ubicacion`
Se creó una segunda entidad llamada `Ubicacion` para evitar guardar la ubicación como texto libre dentro del objeto.

La relación establecida es:
- `Ubicacion 1 --- N ObjetoEncontrado`

Esto significa que:
- una ubicación puede tener muchos objetos
- cada objeto pertenece a una sola ubicación
- la relación se gestiona con una foreign key desde `ObjetoEncontrado` hacia `Ubicacion`

### 3. Manager y QuerySet
Se implementaron clases adicionales para manejar la lógica de búsqueda:
- `ObjetoEncontradoQuerySet`
- `ObjetoEncontradoManager`

Esto permite hacer consultas reutilizables y ordenadas, como por ejemplo buscar objetos por nombre o ubicación sin repetir la misma lógica en cada vista.

### 4. Persistencia con SQLite y migraciones
Se configuró la app para que los datos se almacenen en SQLite mediante migraciones de Django.

Además, se agregaron datos iniciales de ejemplo para preservar la lógica de la Semana 2, pero ahora almacenados de forma persistente en la base de datos.

### 5. Formularios
Se reemplazó el formulario básico por un `ModelForm` orientado al ORM.

También se creó un formulario para crear nuevas ubicaciones desde la interfaz, para que el usuario pueda registrar una ubicación nueva y luego seleccionarla al momento de crear el objeto.

### 6. Vistas y rutas
Las vistas de listado, detalle y creación fueron adaptadas para trabajar con el ORM:
- listado de objetos
- detalle del objeto
- creación de objetos
- creación de ubicaciones

Las rutas quedaron organizadas en `urls.py` para que el flujo de la aplicación siga funcionando sin necesidad de crear un proyecto nuevo.

### 7. Templates HTML
Se actualizaron los templates para que:
- muestren la ubicación con su nombre real
- permitan navegar entre el listado y el detalle
- incluyan un enlace para crear una nueva ubicación desde la pantalla de registro

### 8. Pruebas de validación
Se añadieron pruebas en `tests.py` para verificar:
- que se pueden crear objetos
- que la búsqueda por nombre o ubicación funciona
- que la relación entre `Ubicacion` y `ObjetoEncontrado` se mantiene correctamente

---

## Estructura actual del proyecto

```
semana2/
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── migrations/
│   ├── 0001_initial.py
│   ├── 0002_ubicacion_alter_objetoencontrado_ubicacion.py
│   └── 0003_alter_objetoencontrado_ubicacion.py
├── README.md
├── tests.py
├── urls.py
├── views.py
├── templates/
│   └── semana2/
│       ├── objeto_list.html
│       ├── objeto_detail.html
│       ├── objeto_create.html
│       └── ubicacion_create.html
```

---

## Cómo funciona la aplicación

### Registrar un objeto
1. Ir a `/objetos/objeto/nuevo/`
2. Completar los datos del objeto
3. Elegir la ubicación desde el selector
4. Si la ubicación no existe, crearla antes desde el enlace disponible
5. Guardar

### Ver objetos
1. Ir a `/objetos/`
2. Se listan todos los objetos registrados
3. También se puede buscar por nombre o ubicación

### Consultar detalles
1. Hacer clic en “Ver detalles” dentro de la tabla
2. Se muestra la información completa del objeto

---

## Resultado logrado

Se cumplió la migración desde una solución basada en memoria a una aplicación con:
- Django ORM
- modelos reales
- relación 1:N entre ubicaciones y objetos
- SQLite persistente
- migraciones
- interfaz para registrar ubicación y objetos

---

## Comandos útiles

### Iniciar el servidor
```bash
cd src
python manage.py runserver
```

### Aplicar migraciones
```bash
cd src
python manage.py migrate
```

### Ejecutar pruebas
```bash
cd src
python manage.py test semana2
```

---

## Estado final

La aplicación quedó lista para funcionar como una versión persistente y más organizada de la Semana 2, cumpliendo con la relación solicitada entre las dos entidades principales: `Ubicacion` y `ObjetoEncontrado`.
