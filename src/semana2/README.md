# Semana 2 — Sistema de Objetos Encontrados

## Descripción

Aplicación Django para registrar y visualizar objetos encontrados en una institución educativa. Permite a estudiantes, docentes y personal registrar objetos hallados con información de ubicación, fecha y contacto.

## Estructura de archivos

```
semana2/
├── __init__.py
├── admin.py              # No utiliza admin (sin base de datos)
├── apps.py               # Configuración de la app
├── forms.py              # Formulario ObjetoEncontradoForm
├── models.py             # Datos en memoria (lista de diccionarios)
├── tests.py              # Tests (vacío)
├── urls.py               # Rutas de la app
├── views.py              # Vistas (list, detail, create)
└── templates/semana2/
    ├── objeto_list.html      # Listado de objetos
    ├── objeto_detail.html    # Detalles de un objeto
    └── objeto_create.html    # Formulario de creación
```

## Características implementadas

### 1. Listado de objetos encontrados
- **URL:** `/objetos/`
- **Vista:** `objeto_list`
- Muestra todos los objetos en una tabla con:
  - Nombre
  - Descripción
  - Ubicación
  - Fecha encontrado
  - Contacto
  - Enlace a detalles
- **Búsqueda integrada:** Campo para buscar por nombre o ubicación (case-insensitive)

### 2. Detalles de un objeto
- **URL:** `/objetos/objeto/<id>/`
- **Vista:** `objeto_detail`
- Muestra información completa del objeto con formato de definición

### 3. Crear nuevo objeto
- **URL:** `/objetos/objeto/nuevo/`
- **Vista:** `objeto_create` (GET y POST)
- Formulario con validaciones:
  - **Nombre:** Requerido, máximo 200 caracteres
  - **Descripción:** Requerido, mínimo 5 caracteres
  - **Ubicación:** Requerido, máximo 200 caracteres
  - **Fecha:** Requerido, formato DD/MM/YYYY validado
  - **Contacto:** Requerido, máximo 200 caracteres

### 4. Buscar objetos
- **Integrada en:** `/objetos/`
- Búsqueda por nombre o ubicación (case-insensitive)
- Parámetro GET: `?q=término`
- Muestra cantidad de resultados encontrados
- Enlace para limpiar búsqueda

## Datos en memoria

Los datos se almacenan en `models.py` como una lista de diccionarios con **10 ejemplos iniciales**:

```python
objetos_encontrados = [
    {
        "id": 1,
        "nombre": "Mochila negra",
        "descripcion": "Mochila negra con cuadernos y bolígrafos",
        "ubicacion": "Biblioteca",
        "fecha": "25/08/2026",
        "contacto": "Ana Torres"
    },
    # ... 9 objetos más
]
```

**Ejemplos disponibles:**
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

## ⚠️ IMPORTANTE: Persistencia de datos

**LOS DATOS SE PIERDEN AL REINICIAR EL SERVIDOR**

Esta aplicación NO utiliza base de datos. Los registros se mantienen únicamente en memoria durante la ejecución del servidor. Al detener y reiniciar Django:

- ❌ Se pierden todos los objetos agregados durante la sesión
- ✅ Se reestablecen los 5 registros de ejemplo iniciales

Esto es esperado y forma parte del diseño de esta versión inicial.

## Funciones auxiliares en models.py

```python
obtener_objetos()           # Retorna lista completa
obtener_objeto_por_id(id)   # Busca un objeto por ID
agregar_objeto(...)         # Agrega nuevo objeto a la lista
buscar_objetos(termino)     # Busca por nombre o ubicación
```

## Formulario personalizado

El formulario `ObjetoEncontradoForm` en `forms.py`:
- Hereda de `django.forms.Form` (no ModelForm)
- Incluye validaciones personalizadas con métodos `clean_*`
- Valida formato de fecha DD/MM/YYYY
- Valida longitud mínima de descripción
- Renderiza errores en la plantilla

## Cómo usar

### Iniciar el servidor
```bash
cd src
python manage.py runserver
```

### Acceder a la aplicación
- Listado: http://127.0.0.1:8000/objetos/
- Nuevo objeto: http://127.0.0.1:8000/objetos/objeto/nuevo/
- Detalles: http://127.0.0.1:8000/objetos/objeto/1/

### Crear un nuevo objeto
1. Ir a `/objetos/objeto/nuevo/`
2. Completar el formulario con datos válidos
3. Hacer clic en "Registrar objeto"
4. Confirmar que aparece en el listado

### Buscar objetos
1. En el listado `/objetos/`, completar el campo "Buscar por nombre o ubicación"
2. Hacer clic en "Buscar"
3. Se mostrarán solo los objetos que coincidan
4. Hacer clic en "Limpiar" para volver a ver todos

## Requisitos completados

- ✅ Registrar objetos encontrados (Req. 1)
- ✅ Visualizar objetos encontrados (Req. 2)
- ✅ Consultar información de un objeto (Req. 3)
- ✅ Buscar objetos (Req. 4)
- ✅ Registrar datos de contacto (Req. 5)

## Futuras ampliaciones

- Agregar filtros avanzados (por fecha, contacto)
- Ordenamiento de resultados (por fecha, nombre)
- Persistencia en base de datos (migrar de lista a Django ORM)
- Autenticación de usuarios
- Formulario de contacto para recuperar objetos
- Notificaciones por email
- Exportar datos a PDF o Excel
