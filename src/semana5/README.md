# Semana 4 - Modelo de datos ampliado

Esta aplicación amplía el sistema de la óptica con relaciones entre entidades, consultas optimizadas y CRUD para el modelo intermedio.

## Repositorio

URL del repositorio en GitHub:

<https://github.com/adrienyldefonso-sys/mydjango.git>

## Entidades

La aplicación `semana4` contiene siete entidades:

- `Cliente`: datos personales del paciente.
- `Optometrista`: profesional responsable de la atención.
- `Sucursal`: sede de la óptica.
- `Producto`: armazones, lunas y lentes de contacto.
- `HistorialClinico`: exámenes y diagnósticos de un cliente.
- `FichaMedica`: información médica complementaria de un cliente.
- `Venta`: modelo intermedio que registra la relación entre clientes y productos.

## Relaciones

### Relación 1:N: Cliente e HistorialClinico

Cada historial clínico pertenece a un cliente y un cliente puede tener varios historiales:

```python
class HistorialClinico(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='historiales'
    )
```

Acceso directo:

```python
historial.cliente
```

Acceso inverso:

```python
cliente.historiales.all()
```

### Relación 1:1: Cliente y FichaMedica

Cada cliente puede tener una única ficha médica:

```python
class FichaMedica(models.Model):
    cliente = models.OneToOneField(
        Cliente,
        on_delete=models.CASCADE,
        related_name='ficha_medica'
    )
```

Acceso desde la ficha:

```python
ficha.cliente
```

Acceso inverso desde el cliente:

```python
cliente.ficha_medica
```

### Relación N:M: Cliente y Producto mediante Venta

Un cliente puede comprar varios productos y un producto puede ser vendido a varios clientes. La relación se implementa con `Venta` como modelo intermedio, porque la relación tiene atributos propios:

```python
class Cliente(models.Model):
    productos = models.ManyToManyField(
        'Producto',
        through='Venta',
        related_name='clientes'
    )
```

```python
class Venta(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='ventas'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='ventas'
    )
    fecha_venta = models.DateField()
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
```

Recorridos disponibles:

```python
cliente.productos.all()
cliente.ventas.all()
venta.producto
producto.ventas.all()
```

## Consultas relacionadas

Las vistas utilizan `select_related()` para relaciones de una sola fila y `prefetch_related()` para relaciones de varios registros:

```python
Cliente.objects.select_related(
    'ficha_medica'
).prefetch_related(
    'historiales',
    'ventas__producto'
)
```

Ejemplos utilizados:

- `select_related('ficha_medica')`: obtiene la ficha médica con un `JOIN` SQL.
- `select_related('cliente', 'producto')`: obtiene el cliente y producto de cada venta con `JOIN`.
- `prefetch_related('historiales')`: carga los historiales relacionados en una consulta adicional.
- `prefetch_related('ventas__producto')`: carga las ventas y sus productos relacionados evitando consultas N+1.

## Recorrido de una consulta

Para `/optica-v2/clientes/relacionados/`:

```text
Request
  -> config/urls.py
  -> semana4/urls.py
  -> lista_clientes_relacionados()
  -> Cliente.objects.select_related().prefetch_related()
  -> SQLite
  -> contexto {'clientes': clientes}
  -> cliente_list.html
  -> Response HTML
```

La relación interviene en `ventas__producto`: desde cada `Cliente` se recorren sus objetos `Venta` y, desde cada venta, su `Producto`.

## CRUD de Venta

El modelo intermedio se puede administrar desde estas rutas:

```text
GET  /optica-v2/ventas/                 Listado de ventas
GET  /optica-v2/ventas/nueva/           Formulario de creación
POST /optica-v2/ventas/nueva/           Inserta una venta
GET  /optica-v2/ventas/<id>/editar/     Formulario de edición
POST /optica-v2/ventas/<id>/editar/     Actualiza una venta
GET  /optica-v2/ventas/<id>/eliminar/   Confirmación de eliminación
POST /optica-v2/ventas/<id>/eliminar/  Elimina una venta
```

Los atributos propios de la relación son `fecha_venta`, `cantidad`, `precio_unitario` y `estado`.

## Migraciones

La migración inicial se encuentra en `migrations/0001_initial.py` y crea las tablas de las siete entidades, las claves foráneas y la relación N:M con `through`.

Desde la carpeta `src`:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
```

Las migraciones aplicadas aparecen con `[X]`.

## Verificación

```powershell
python manage.py check
python manage.py test semana4
```

Actualmente la aplicación no contiene pruebas automatizadas específicas, por lo que el comando de tests puede indicar `Ran 0 tests`.
