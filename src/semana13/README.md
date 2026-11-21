# Semana 13 — Proyecto integrador Ojo d’Chakra

Este documento adapta el laboratorio al proyecto integrador **Ojo d’Chakra**, usando lo que ya se desarrolló en las semanas anteriores. El proyecto actual es un panel agronómico para consultar y administrar diagnósticos asociados a parcelas; no es una tienda en línea.

## Ejercicio 1 — Tipos de comercio y canales

| Tipo | Quién vende a quién | Ejemplo peruano | Relación con Ojo d’Chakra |
|---|---|---|---|
| B2C (Business to Consumer) | Una empresa vende directamente a una persona consumidora. | Tambo+ ofrece productos a consumidores finales. | No está implementado. Podría aplicar en el futuro si el proveedor ofreciera el servicio directamente a agricultores individuales. |
| B2B (Business to Business) | Una empresa vende productos o servicios a otra empresa u organización. | Alicorp provee productos e insumos a restaurantes y tiendas. | Es el modelo más cercano si una empresa ofreciera Ojo d’Chakra como servicio a cooperativas o empresas agrícolas. Esa venta no existe en la aplicación actual. |
| C2C (Consumer to Consumer) | Una persona vende directamente a otra persona, normalmente mediante una plataforma que las conecta. | Una persona ofrece un artículo usado a otra mediante Facebook Marketplace en Perú. | No está implementado: el sistema no conecta agricultores para que se vendan productos o servicios entre sí. |

### ¿Qué tipo corresponde a Ojo d’Chakra?

La versión construida **no implementa una transacción comercial**: no hay catálogo de productos en venta, precios, pagos ni pedidos. Por eso, Ojo d’Chakra no se clasifica actualmente como B2C, B2B o C2C; es una aplicación de gestión y consulta de información agronómica.

Si en el futuro una empresa ofrece Ojo d’Chakra como servicio a cooperativas, empresas agrícolas o productores organizados, el modelo comercial más cercano sería **B2B**. Esa relación de venta sería una posibilidad de negocio futura, no una función implementada en el proyecto.

### Canales

- **Web — implementado:** el panel de React consulta la API REST de Django mediante Axios.
- **Móvil — posible extensión:** una aplicación móvil podría consumir los mismos endpoints de la API. No hay un cliente móvil implementado en las semanas revisadas.
- **Redes sociales — posible integración:** podrían servir para difundir información o enlazar al panel; una integración que intercambie datos con la API todavía no está implementada.

El **m-commerce** describe el canal o dispositivo de compra (por ejemplo, un teléfono móvil), mientras que el **social commerce** describe el uso de una red social como canal para descubrir o realizar una compra. No determinan quién vende a quién. En Ojo d’Chakra estos términos no describen funciones actuales, porque el sistema no vende ni procesa compras.

## Base existente del proyecto integrador

### Lo desarrollado en semanas anteriores

- **Semana 11:** backend de práctica Django REST Framework y un frontend de prueba con datos mock. El backend define las entidades `Parcela` y `Diagnostico`, sus serializers, validaciones y endpoints.
- **Semana 12, Parte 2:** el frontend React/Vite conecta el panel Ojo d’Chakra con el backend de Semana 11 mediante la instancia Axios `apiOjoChakra`. Incluye consulta, búsqueda, filtro, resumen y operaciones CRUD de diagnósticos.
- **Semana 13:** se creó una copia de trabajo independiente del backend de Ojo d’Chakra en `src/semana13/backend`, con su propia app `historial` y base SQLite. No cambia la conexión del frontend de Semana 12, que sigue apuntando al backend de Semana 11.
- **Semana 12, Parte 1:** es una práctica separada que consulta la API de productos de óptica de Semana 8. No forma parte de Ojo d’Chakra.

El componente llamado `Carrito` en el panel solo guarda diagnósticos seleccionados en el estado de React y calcula unidades y suma de confianza. No representa un carrito de compras: no maneja precios ni pagos y no envía pedidos.

## Ejercicio 2 — Módulos y roles de Ojo d’Chakra

El mapa de módulos del proyecto integrador queda así:

```text
Ojo d’Chakra
├── Parcelas
├── Diagnósticos e historial
├── Búsqueda, filtros y resumen
├── Panel administrativo propio
├── Usuarios, roles y seguridad (pendiente)
└── Notificaciones (pendiente)
```

| Módulo del enunciado | Equivalente en Ojo d’Chakra | Estado / semana |
|---|---|---|
| Catálogo | Parcelas y diagnósticos disponibles para consulta. | Modelos y API en S11; consulta desde React en S12. |
| Carrito | No aplica como módulo de compra. El componente `Carrito` de S12 solo selecciona diagnósticos temporalmente en el estado de React; no cobra ni crea pedidos. | Prototipo local en S12. |
| Usuarios y roles | Cuentas para agricultores y administradores, con acceso según su rol. | No implementado. Propuesta: S14. |
| Pedidos | No aplica: el sistema no recibe ni procesa compras. | No aplica al integrador actual. |
| Pagos | No aplica: no hay precios ni cobros. | No aplica al integrador actual. |
| Inventario | No hay existencias de productos. El módulo relevante es la consulta de parcelas, que no equivale a inventario. | Parcelas: modelo y consulta API en S11; visualización en S12. |
| Panel administrativo | Panel propio para revisar, buscar, crear, editar y eliminar diagnósticos. | API en S11; interfaz CRUD en S12. |
| Seguridad | Inicio de sesión, permisos por rol y restricción de datos por agricultor/parcela. | No implementado. Propuesta: S14, junto con usuarios y roles. |
| Notificaciones | Avisos sobre nuevos diagnósticos o cambios. El `Aviso` actual es solo un mensaje temporal de interfaz. | No hay notificaciones persistentes. Propuesta: S16. |
| Mejoras de gestión | Completar el mantenimiento de parcelas y ajustar las pantallas a cada rol. | Propuesta: S15. |

La planificación de S14–S16 es una propuesta para completar el integrador; debe ajustarse si el cronograma indicado por el docente asigna esas semanas de otra manera. Lo ya construido en S11–S12 se conserva y reutiliza.

### Roles y pantallas

La siguiente tabla describe los permisos que convendría implementar. Actualmente no hay inicio de sesión ni autorización por rol: la pantalla de Ojo d’Chakra y la API de práctica no distinguen estos perfiles.

| Rol | Qué puede hacer | Qué pantalla usa |
|---|---|---|
| Visitante | En el diseño propuesto, ver una pantalla pública de presentación e iniciar sesión; no consultar ni modificar historiales privados. | Página pública o inicio de sesión; aún no implementada. |
| Agricultor (equivalente al cliente del enunciado) | Consultar las parcelas que tiene asignadas y revisar, buscar y filtrar sus diagnósticos. No debería modificar datos de otras personas. | Panel de diagnósticos e historial de su parcela. La pantalla existe en S12, pero la asignación y restricción por usuario están pendientes. |
| Administrador | Gestionar parcelas y diagnósticos, y administrar usuarios y permisos. | Panel administrativo propio. El CRUD de diagnósticos existe en S12; la gestión de usuarios, parcelas y permisos está pendiente. |

En el modelo actual, `agricultor` es un campo de texto de `Parcela`, no una cuenta de usuario. Por eso, los roles y permisos de la tabla son el diseño propuesto y no capacidades de seguridad ya implementadas.

## Ejercicio 3 — Requisitos de Ojo d’Chakra

Estos requisitos se redactan para el proyecto integrador. Los criterios describen cómo comprobar cada requisito. Los de seguridad y rendimiento son objetivos propuestos; no se consideran implementados ni verificados en las semanas anteriores.

### Requisitos funcionales

| ID | Descripción | Prioridad | Criterio de aceptación |
|---|---|---|---|
| RF-01 | El sistema debe mostrar las parcelas registradas con nombre, cultivo, agricultor y ubicación. | Alta | Al consultar `GET /api/parcelas/`, la respuesta es HTTP 200 y cada parcela incluye esos campos. |
| RF-02 | El usuario debe poder consultar los diagnósticos asociados a una parcela y un resumen de sus resultados. | Alta | Al seleccionar una parcela, solo se muestran diagnósticos asociados a ella y el resumen coincide con el total y los conteos visibles. |
| RF-03 | El usuario debe poder buscar diagnósticos por nombre o código de plaga y filtrar por el código de plaga. | Alta | Al buscar un texto, cada resultado coincide con el nombre o código; al elegir un código, solo aparecen diagnósticos con ese código. |
| RF-04 | El administrador debe poder registrar y editar un diagnóstico con parcela, fecha, plaga, confianza e imagen opcional. | Alta | Un registro válido se crea con HTTP 201 y una edición válida se guarda con HTTP 200; una confianza fuera de 0–100 se rechaza con HTTP 400. |
| RF-05 | El administrador debe poder eliminar un diagnóstico después de confirmar la acción. | Media | Al cancelar la confirmación no se envía DELETE; al confirmar, la API responde HTTP 204 y el diagnóstico deja de aparecer en la lista. |

RF-01, RF-03, RF-04 y RF-05 corresponden a capacidades presentes en la API o el panel de S11–S12. RF-02 describe el resultado esperado del panel; la interfaz calcula el resumen de los diagnósticos consultados. La separación de resultados por usuario y parcela dependerá de implementar autenticación y permisos.

### Requisitos no funcionales

| ID | Descripción | Prioridad | Criterio de aceptación |
|---|---|---|---|
| RNF-01 | El listado de diagnósticos debe responder con rapidez bajo una carga definida. | Alta | Con 1,000 diagnósticos y 20 solicitudes concurrentes, el percentil 95 de `GET /api/diagnosticos/` debe ser de 2 segundos o menos, medido con una prueba de carga. |
| RNF-02 | La API debe autenticar a sus usuarios y autorizar las operaciones según su rol y sus parcelas asignadas. | Alta | Sin credenciales, las operaciones protegidas responden HTTP 401; un agricultor que intente acceder a una parcela ajena recibe HTTP 403, y un administrador autorizado puede gestionar los registros. |
| RNF-03 | El panel debe poder utilizarse en las versiones actuales de Chrome y Edge, tanto en escritorio como en un móvil. | Media | Las funciones de consulta y administración se completan en ambos navegadores a 360 px y 1280 px de ancho, sin contenido cortado ni desplazamiento horizontal de la página. |
| RNF-04 | Los controles y mensajes del panel deben ser accesibles mediante teclado y tener nombres comprensibles para tecnologías de asistencia. | Media | Se puede recorrer y activar cada control con teclado; los campos tienen etiquetas y los errores se anuncian como mensajes de alerta. |
| RNF-05 | Los diagnósticos guardados deben persistir en la base de datos y mantenerse disponibles después de reiniciar Django. | Alta | Se crea un diagnóstico, se reinicia el servidor y una consulta posterior devuelve el mismo identificador y los mismos datos. |

### Diferencia entre requisitos funcionales y no funcionales

Un requisito **funcional** indica qué operación o servicio ofrece el sistema, por ejemplo, buscar diagnósticos o registrar uno nuevo. Un requisito **no funcional** establece cómo debe funcionar o qué nivel de calidad debe cumplir, por ejemplo, el tiempo de respuesta, la seguridad o la compatibilidad.

### Reescritura de “El sistema debe ser rápido y seguro”

- **Rendimiento:** “Con hasta 1,000 diagnósticos y 20 solicitudes concurrentes, el percentil 95 de respuesta de `GET /api/diagnosticos/` será de 2 segundos o menos, medido mediante una prueba de carga.”
- **Seguridad:** “Las operaciones protegidas de la API exigirán autenticación; las solicitudes sin credenciales recibirán HTTP 401 y un agricultor que solicite una parcela no asignada recibirá HTTP 403.”

Estos son criterios propuestos para el integrador. Actualmente, el backend de práctica usa `AllowAny` y no implementa cuentas, roles ni restricciones por parcela, por lo que el requisito de seguridad todavía no se cumple.

### Reglas de negocio existentes

| Regla | Dónde se aplica |
|---|---|
| La confianza de un diagnóstico debe estar entre 0 y 100, con hasta dos decimales. | Validadores del modelo y `validate_confianza` del serializer. |
| La latitud debe estar entre -90 y 90, y la longitud entre -180 y 180. | Validadores del modelo `Parcela`. |
| Cada diagnóstico debe pertenecer a una parcela. | Campo `ForeignKey` del modelo `Diagnostico`; eliminar una parcela elimina sus diagnósticos relacionados. |

## Ejercicio 4 — Arquitectura y flujo de Ojo d’Chakra

Este ejercicio se desarrolla únicamente con el proyecto integrador Ojo d’Chakra.

### Arquitectura implementada

```text
Agricultor / usuario
        │
        │ interacción con la interfaz
        ▼
React: panel de Ojo d’Chakra (Semana 12)
        │ Axios — HTTP (GET/POST/PATCH/DELETE) y JSON
        ▼
Django URL: /api/
        │ enruta la petición
        ▼
DRF View / ViewSet
        │ llama al serializer
        ▼
Serializer: valida datos y convierte entre objetos y JSON
        │ datos validados
        ▼
Django ORM — consultas SQL
        │
        ▼
SQLite
        │ resultado de la consulta o escritura
        └───────────────────────────────────────────┐
                                                    ▼
React recibe JSON + estado HTTP y actualiza la pantalla
```

Entre React y Django viajan solicitudes y respuestas HTTP; los datos de la API están en JSON. Dentro del servidor, Django usa el ORM para consultar o modificar SQLite: no se envían objetos ORM al navegador.

### Flujo real del integrador

| Paso | Qué hace React | Qué hace Django / estado resultante |
|---|---|---|
| 1. Abrir el panel | Solicita `GET /api/parcelas/` mediante Axios. | La vista serializa las parcelas y responde JSON con HTTP 200. |
| 2. Cargar el historial | Selecciona la primera parcela recibida y solicita `GET /api/diagnosticos/?parcela=<uuid>`. | El ViewSet filtra los diagnósticos por parcela; responde con JSON y HTTP 200. |
| 3. Explorar y filtrar | Muestra los diagnósticos; búsqueda y filtro vuelven a consultar la API con `search` o `plaga_detectada`. | Aplica los filtros solicitados; la consulta no modifica datos. |
| 4. Registrar o editar | Envía `POST /api/diagnosticos/` o `PATCH /api/diagnosticos/<uuid>/` con JSON. | El serializer valida los campos; guarda con el ORM si son válidos (HTTP 201 al crear, HTTP 200 al actualizar) o responde HTTP 400 si no lo son. |
| 5. Eliminar | Solicita confirmación y, si se confirma, envía `DELETE /api/diagnosticos/<uuid>/`. | Elimina el diagnóstico y responde HTTP 204; React lo quita de la lista. |

El estado de cada operación se representa en la interfaz con carga, resultado o error. El modelo no incluye compras, pedidos ni entregas.

El panel de Semana 12 usa el backend de `src/semana11/backend` en `127.0.0.1:8001`; su instancia Axios apunta a `http://127.0.0.1:8001/api`. Semana 13 tiene una copia independiente que puede ejecutarse en `127.0.0.1:8002`. El backend de práctica de Semana 11 usa `AllowAny` según la documentación de Semana 12; antes de exponer cualquiera de estos backends en un entorno real se deben configurar autenticación y permisos.

### ¿Se puede implementar una pasarela de pago?

En la versión actual **no corresponde integrar una pasarela**: Ojo d’Chakra registra y consulta parcelas y diagnósticos; no vende productos, no cobra por operación y no administra pedidos. Por tanto, en el flujo actual no hay número de tarjeta, token de pago ni confirmación de compra que describir.

Técnicamente sí podría añadirse en el futuro si se define un servicio cobrable —por ejemplo, una suscripción para cooperativas o funciones premium— y sus reglas de negocio. Eso requeriría diseñar planes, cuentas y permisos, estados de suscripción y la relación entre el pago confirmado y el acceso al sistema. Sería una nueva función, no una necesidad del flujo actual de diagnósticos.

Si se implementara ese modelo, el número de tarjeta y el CVV deberían ingresarse directamente en el checkout seguro de la pasarela, no en React ni en Django. La pasarela devolvería al backend una referencia/token y el resultado del pago para asociarlos a la suscripción. Así Ojo d’Chakra no almacenaría datos completos de tarjeta.

## Ejercicio 5 — Reglas de negocio y errores comunes

Las reglas se adaptan a Ojo d’Chakra. Precio, inventario comercial y datos de tarjeta no existen en el integrador; se indica dónde no aplican para no atribuirle funciones que no tiene.

| Regla de negocio | Dónde se aplica | Qué error evita |
|---|---|---|
| La parcela y los diagnósticos válidos se leen y guardan en la base de datos a través de Django; React no es la fuente oficial de esos datos. | Django: ORM, vistas y serializers. React presenta la respuesta y envía cambios. | Mostrar o guardar datos manipulados o desactualizados como si fueran oficiales. |
| Cada diagnóstico debe pertenecer a una parcela existente. Ojo d’Chakra no maneja stock de productos. | Django: relación `ForeignKey` y validación del serializer. | Asociar un diagnóstico a una parcela inexistente o confundir el sistema con un inventario comercial. |
| La confianza del diagnóstico es un decimal entre 0 y 100, con dos posiciones decimales; no debe tratarse como dinero ni como `float` impreciso. | Django: `DecimalField` en el modelo y validación del serializer. React adapta el valor para mostrarlo y editarlo. | Guardar confianza fuera de rango o introducir redondeos imprecisos. |
| No se solicitan ni almacenan números de tarjeta o CVV, porque el sistema no procesa pagos. | No aplica en la versión actual. Si se agrega una suscripción, la pasarela procesa la tarjeta y Django guarda solo la referencia y el estado del pago. | Exponer información financiera sensible sin necesidad. |
| La selección temporal del componente `Carrito` no es un diagnóstico guardado ni una compra: solo un `POST` válido crea un diagnóstico persistente. | React mantiene la selección local; Django valida y persiste el diagnóstico cuando recibe el `POST`. | Confundir una selección temporal de diagnósticos con datos persistidos, pedidos o pagos. |

### ¿Por qué una regla de stock no puede controlarse solo en React?

Ojo d’Chakra no administra stock, así que no hay una regla de inventario que implementar. El principio equivalente es que las reglas que protegen los datos deben validarse en Django: el navegador puede modificarse y distintos clientes pueden enviar solicitudes directamente a la API, sin usar la interfaz React. La validación del serializer y las restricciones del modelo/base de datos evitan depender de controles que solo existen en pantalla. Para el stock de una aplicación que sí lo maneje, el servidor también tendría que comprobar y actualizar las existencias de forma atómica para evitar que solicitudes simultáneas vendan las mismas unidades.

## Ejercicio 6 — Apps Django de Ojo d’Chakra

Para este proyecto **no corresponde crear las apps `catalogo` y `pedidos`**: Ojo d’Chakra no tiene un catálogo comercial ni pedidos. Para practicar la estructura del backend sin modificar Semana 11, se creó en Semana 13 un proyecto Django independiente con una app `historial`.

La app `historial` reúne los modelos `Parcela` y `Diagnostico`, sus serializers, vistas, pruebas y rutas de API. La estructura creada es:

```text
semana13/backend/
├── manage.py
├── config/                         Proyecto Django
│   ├── settings.py                 Registra historial y DRF en INSTALLED_APPS
│   └── urls.py                     Monta historial bajo /api/
├── historial/                      App de Ojo d’Chakra
│   ├── migrations/                 Esquema de Parcela y Diagnostico
│   ├── models.py                   Modelos Parcela y Diagnostico
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── requirements.txt
└── .gitignore                      Excluye SQLite y archivos generados
```

En `src/semana13/backend/config/settings.py`, `INSTALLED_APPS` incluye Django, Django REST Framework, CORS y la app del integrador:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'core.apps.CoreConfig',
    'parcelas.apps.ParcelasConfig',
    'diagnosticos.apps.DiagnosticosConfig',
    'historial.apps.HistorialConfig',
]
```

El backend de Semana 13 es independiente del de Semana 11. Para crear su base de datos local, comprobarlo y ejecutar sus pruebas, desde la raíz del repositorio:

```powershell
cd .\src\semana13\backend
python manage.py migrate
python manage.py check
python manage.py test historial
```

La comprobación `python manage.py check` obtuvo esta salida:

```text
System check identified no issues (0 silenced).
```

Para iniciar esta copia del backend sin ocupar el puerto usado por Semana 11:

```powershell
python manage.py runserver 127.0.0.1:8002
```

La API estará disponible en `http://127.0.0.1:8002/api/`. El frontend de Semana 12 no se cambió y seguirá usando el backend de Semana 11 en el puerto `8001`.

Un **proyecto Django** es la configuración global que conecta settings, URLs y la ejecución del servidor. Una **app Django** es un módulo con una responsabilidad funcional, como `historial`, que contiene modelos, vistas, serializers y rutas del dominio agronómico. Un proyecto puede incluir varias apps; en esta copia de Semana 13, `historial` implementa las parcelas y sus diagnósticos.

## Ejercicio 7 — Estructura inicial de React

La estructura se adaptó al dominio de Ojo d’Chakra: se crearon `DiagnosticoCard.jsx` y `DiagnosticosPage.jsx` en vez de componentes de productos. La página consulta la lista de diagnósticos; la tarjeta muestra cada resultado. `api.js` centraliza Axios y apunta al backend independiente de Semana 13.

```text
semana13/frontend/
├── .gitignore
├── index.html
├── package.json
├── package-lock.json
├── vite.config.js
└── src/
    ├── api.js
    ├── App.jsx
    ├── main.jsx
    ├── components/
    │   └── DiagnosticoCard.jsx
    └── pages/
        ├── DiagnosticosPage.jsx
        ├── ParcelasPage.jsx
        ├── HistorialParcelaPage.jsx
        └── DiagnosticoFormPage.jsx
```

- **`components/`:** componentes reutilizables de interfaz. `DiagnosticoCard.jsx` presenta los datos de un diagnóstico.
- **`pages/`:** pantallas completas que organizan componentes y datos. `DiagnosticosPage.jsx` consulta y muestra la lista de diagnósticos.
- **`api.js`:** crea una instancia Axios compartida, para centralizar la URL base y el timeout de las solicitudes a Django.

La instancia actual de `api.js` usa `http://127.0.0.1:8002/api/`, porque ese es el puerto del backend de Semana 13. `App.jsx` configura la ruta React `/diagnosticos`; `DiagnosticosPage.jsx` solicita `GET /api/diagnosticos/` con `api.get('diagnosticos/')`. Los paquetes y comandos `dev` y `build` están declarados en `frontend/package.json`.

## Ejercicio 8 — Mapa de rutas y verificación

El backend de Semana 11 y la copia independiente de Semana 13 exponen las mismas rutas API; cambia el puerto: Semana 11 usa `8001` y Semana 13 usa `8002`. La ruta React `/diagnosticos` está implementada; las demás rutas React de la tabla son el mapa propuesto para las pantallas que aún faltan.

| Recurso | Ruta de la API de Django | Ruta de React |
|---|---|---|
| Listar parcelas | `GET /api/parcelas/` | `/parcelas` (propuesta; página pendiente) |
| Historial de una parcela | `GET /api/parcelas/<uuid>/historial/` | `/parcelas/:id/historial` (propuesta; página pendiente) |
| Listar y crear diagnósticos | `GET` o `POST /api/diagnosticos/` | `/diagnosticos` (página implementada para listar; alta pendiente) |
| Consultar, editar o eliminar un diagnóstico | `GET`, `PUT`, `PATCH` o `DELETE /api/diagnosticos/<uuid>/` | `/diagnosticos` (la ruta de detalle opera desde la lista; acciones pendientes) |
| Buscar y filtrar diagnósticos | Parámetros `parcela`, `search`, `plaga_detectada`, `ordering`, `desde` y `hasta` en `/api/diagnosticos/` | `/diagnosticos?search=...` (propuesta; filtros pendientes) |

La ruta API identifica un recurso del backend: Axios envía una petición HTTP y Django responde, normalmente con JSON y un estado HTTP. La ruta React es una dirección del frontend que React Router usa para decidir qué pantalla mostrar; por sí sola no consulta ni modifica la base de datos. El frontend de Semana 12 cambia de sección mediante estado y no usa rutas URL de React Router; el frontend inicial de Semana 13 sí configura `/diagnosticos`.

### Verificación del backend

Se inició el backend de Semana 13 desde `src/semana13/backend`:

```powershell
python manage.py runserver 127.0.0.1:8002 --noreload
```

La API respondió a `GET http://127.0.0.1:8002/api/parcelas/` con **HTTP 200**. La salida del servidor confirmó la solicitud:

```text
"GET /api/parcelas/ HTTP/1.1" 200 2
```

### Verificación del frontend

Desde `src/semana13/frontend` se ejecutó:

```powershell
npm run build
```

Vite completó la compilación:

```text
vite v8.3.8 building client environment for production...
✓ 83 modules transformed.
dist/index.html                  0.35 kB │ gzip:   0.26 kB
dist/assets/index-CJwNzk3j.js  317.68 kB │ gzip: 103.53 kB
✓ built in 227ms
```

`node_modules/` y `dist/` están excluidos por `frontend/.gitignore`.

## PARTE 2 — Diseño del proyecto integrador

## Ejercicio 9 — Entidad y módulos de Ojo d’Chakra

La entidad principal es **Diagnostico**, relacionada con **Parcela**: cada diagnóstico pertenece a una parcela y registra la plaga detectada, la fecha, la confianza y una URL de imagen opcional. Ambas entidades ya están definidas en `semana13/backend/historial/models.py`; no es necesario inventar otra entidad para continuar con los siguientes ejercicios.

| Concepto | Equivalencia en Ojo d’Chakra | Estado y rutas |
|---|---|---|
| Tipo de comercio | Actualmente no es un comercio: no vende productos ni procesa pagos. Si se ofreciera mediante suscripción a cooperativas o empresas agrícolas, el modelo futuro más cercano sería B2B. | No hay transacciones comerciales implementadas. |
| Entidad principal | `Diagnostico`, relacionado con `Parcela`. | Modelos implementados en `historial/models.py`; API en `/api/diagnosticos/` y `/api/parcelas/`. |
| Módulos | Parcelas; diagnósticos e historial; búsqueda, filtros y resumen; panel administrativo. Usuarios, permisos y notificaciones serían módulos futuros. Pedidos, pagos e inventario comercial no aplican. | API de parcelas e historial y CRUD de diagnósticos implementados. React tiene `/diagnosticos`; una pantalla propia de parcelas aún no está creada. |
| Roles de usuario | Agricultor: consulta sus parcelas e historial. Administrador: gestiona parcelas y diagnósticos. Visitante: solo accede a una página pública o inicio de sesión. | Son roles propuestos: todavía no hay modelo de usuario propio, inicio de sesión ni autorización por rol. |
| Regla de negocio 1 | La confianza del diagnóstico debe estar entre 0 y 100, con dos decimales. | Implementada en el `DecimalField` y en la validación del serializer. |
| Regla de negocio 2 | Cada diagnóstico debe pertenecer a una parcela existente; sus coordenadas deben respetar latitud −90 a 90 y longitud −180 a 180. | La relación y validadores de coordenadas están definidos en los modelos; el serializer valida la parcela referenciada. |
| Rutas API y React | API: `GET /api/parcelas/`, `GET /api/parcelas/<uuid>/historial/` y CRUD en `/api/diagnosticos/`. React: `/diagnosticos` para la lista; `/parcelas` e `/parcelas/:id/historial` quedan propuestas. | La ruta `/diagnosticos` está implementada en Semana 13; las rutas de React de parcelas todavía no. |

El backend de Semana 13 está en `src/semana13/backend` y el frontend independiente en `src/semana13/frontend`. La interfaz React actual solo lista diagnósticos; las operaciones CRUD descritas como parte del integrador corresponden al panel desarrollado en Semana 12 y todavía no todas tienen pantallas en el frontend nuevo de Semana 13.

## Ejercicio 10 — Módulos, requisitos y reglas de negocio

### Mapa de módulos

| Módulo | Responsabilidad | Estado |
|---|---|---|
| Parcelas | Consultar nombre, cultivo, ubicación y agricultor. | Modelo y endpoint de lectura implementados; la pantalla de parcelas en React está pendiente. |
| Diagnósticos e historial | Registrar y consultar plaga, fecha, confianza e imagen asociada a una parcela. | Modelo y API CRUD implementados; el panel completo está en Semana 12 y Semana 13 tiene una página inicial de listado. |
| Búsqueda y filtros | Buscar por nombre o código de plaga, parcela, código exacto y rango de fechas. | Filtros en la API y en el panel de Semana 12; faltan en la página inicial de Semana 13. |
| Resumen | Calcular cantidad de diagnósticos, fecha más reciente y cantidad por plaga. | Historial serializado por la API; el panel de Semana 12 también presenta resumen. |
| Usuarios, roles y permisos | Autenticar y restringir parcelas y operaciones según el rol. | Pendiente; los roles están diseñados, pero no existen cuentas ni permisos específicos. |
| Notificaciones | Informar sobre nuevos diagnósticos o cambios. | Pendiente; los avisos actuales son temporales y solo de interfaz. |

### Tabla de roles

| Rol | Acciones previstas | Pantalla |
|---|---|---|
| Visitante | Ver una presentación pública e iniciar sesión; sin acceso a historiales privados. | Página pública o inicio de sesión, aún pendiente. |
| Agricultor | Consultar las parcelas asignadas y revisar sus diagnósticos. | Panel de parcelas e historial; la vista actual existe, pero aún no limita los datos por usuario. |
| Administrador | Crear y mantener parcelas y diagnósticos, y gestionar usuarios y permisos. | Panel administrativo propio; la gestión de diagnósticos existe en Semana 12, la de usuarios y parcelas está pendiente. |

Estos roles son parte del diseño objetivo. En el modelo actual, `agricultor` es texto en `Parcela`, no una cuenta; la API todavía no aplica autorización por rol.

### Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación verificable |
|---|---|---|---|
| RF-01 | El sistema debe listar las parcelas registradas con nombre, cultivo, agricultor y ubicación. | Alta | `GET /api/parcelas/` responde HTTP 200 y cada objeto contiene esos campos. |
| RF-02 | El usuario debe poder consultar los diagnósticos de una parcela. | Alta | `GET /api/diagnosticos/?parcela=<uuid>` responde solo con diagnósticos asociados al UUID solicitado. |
| RF-03 | El usuario debe poder buscar diagnósticos por nombre o código y filtrarlos por código de plaga. | Alta | Una búsqueda devuelve solo coincidencias; al agregar `plaga_detectada`, todos los resultados tienen ese código exacto. |
| RF-04 | El administrador debe poder crear y actualizar diagnósticos. | Alta | Un `POST` válido responde HTTP 201 y un `PATCH` válido responde HTTP 200; el cambio persiste al volver a consultar. |
| RF-05 | El administrador debe poder eliminar un diagnóstico. | Media | `DELETE /api/diagnosticos/<uuid>/` responde HTTP 204 y una consulta posterior ya no devuelve ese UUID. |

La API implementa estos recursos y operaciones. En el frontend nuevo de Semana 13, por ahora solo está construida la pantalla de listado; formulario, filtros y acciones administrativas se completarán después.

### Requisitos no funcionales

| ID | Requisito | Prioridad | Criterio de aceptación verificable |
|---|---|---|---|
| RNF-01 | Las consultas deben mantener un tiempo de respuesta acotado para un volumen de uso definido. | Media | Con 1,000 diagnósticos y 20 solicitudes concurrentes, el percentil 95 de `GET /api/diagnosticos/` es como máximo 2 segundos, medido con una prueba de carga. |
| RNF-02 | La API debe proteger los datos por autenticación y permisos de parcela. | Alta | Sin credenciales responde HTTP 401; un agricultor que solicite una parcela ajena recibe HTTP 403. Es un criterio futuro: actualmente se usa `AllowAny`. |
| RNF-03 | La interfaz debe ser usable en escritorio y móvil. | Media | En Chrome y Edge, a anchos de 360 px y 1280 px, se pueden completar las acciones disponibles sin contenido cortado ni desplazamiento horizontal de la página. |

### Reglas de negocio

| Regla | Aplicación en React | Aplicación en Django |
|---|---|---|
| La confianza de un diagnóstico debe estar entre 0 y 100, con hasta dos decimales. | El formulario puede restringir y explicar el valor para orientar al usuario. | Regla obligatoria: `DecimalField` y serializer rechazan valores fuera del rango. |
| La latitud debe estar entre −90 y 90 y la longitud entre −180 y 180. | Mostrar coordenadas recibidas; al crear o editar una parcela, validar el formulario antes del envío. | Regla obligatoria: validadores de los campos del modelo `Parcela`. |
| Cada diagnóstico debe pertenecer a una parcela existente. | En el formulario, seleccionar una parcela disponible y enviar su identificador. | Regla obligatoria: relación `ForeignKey`; el serializer verifica que la parcela referenciada exista. |
| La URL de imagen es opcional; si se proporciona, debe tener formato de URL válido. | Permitir dejar el campo vacío y, si se ingresa, usar una entrada de URL con mensaje de validación. | Regla obligatoria: `URLField` del modelo y validación del serializer. |
| Si se consulta el historial con fechas `desde` y `hasta`, ambas deben ser fechas válidas y `desde` no puede ser posterior a `hasta`. | Enviar fechas con formato ISO y evitar que el selector permita un rango invertido. | Regla obligatoria: las vistas del historial y del ViewSet validan el formato y el orden del rango, y responden HTTP 400 si no se cumple. |

React mejora la experiencia con validación inmediata, pero Django debe volver a validar las reglas que protegen los datos porque las solicitudes pueden enviarse directamente a la API sin pasar por la interfaz.
Las validaciones descritas en React son el comportamiento esperado al construir los formularios; la interfaz de Semana 13 todavía solo lista diagnósticos y no implementa formularios de parcelas, diagnósticos ni filtros.

## Ejercicio 11 — Arquitectura y flujo principal

### Arquitectura

```text
Agricultor / administrador
        │
        ▼
React: formulario y panel de diagnósticos
        │ Axios — petición HTTP con JSON
        ▼
Django REST Framework: URL → ViewSet → Serializer
        │ valida parcela, fecha, plaga, confianza e imagen
        ▼
Django ORM
        │ consulta o guarda
        ▼
SQLite
        │ objeto serializado + estado HTTP
        └──────────────────────────► React actualiza el panel
```

### Flujo principal: registrar un diagnóstico

1. **React** recoge la parcela, fecha, código y nombre de la plaga, nivel de confianza y URL de imagen opcional; envía un `POST /api/diagnosticos/` con JSON.
2. **Django REST Framework** enruta la petición al `DiagnosticoViewSet` y valida el JSON con `DiagnosticoSerializer`.
3. En el servidor se comprueba que la parcela exista, que los campos requeridos tengan formato válido, que la confianza esté entre 0 y 100 con hasta dos decimales y que, si se envía, la imagen tenga una URL válida.
4. Si los datos son válidos, el ORM guarda el diagnóstico relacionado con la parcela en SQLite y Django responde **HTTP 201** con el diagnóstico serializado.
5. **React** agrega el registro recibido a la lista y muestra la confirmación. Si falla la validación, Django responde **HTTP 400** con los errores y React los presenta; no se guarda un diagnóstico inválido.

En la interfaz de Semana 13 este formulario todavía está pendiente; el flujo describe la operación ya soportada por la API y el panel integrador de Semana 12.

### Entidades previstas para modelar o completar en Semana 14

- `Usuario`
- `Parcela`
- `Plaga`
- `Diagnostico` — **principal**
- `EvidenciaDiagnostico` — **detalle**

`Parcela` y `Diagnostico` ya tienen modelos iniciales en Semana 11 y en la copia de Semana 13. En Semana 14 se puede revisar y ampliar ese esquema, e incorporar las entidades restantes. `EvidenciaDiagnostico` se plantea como detalle para permitir que un diagnóstico tenga una o más evidencias; hoy el modelo solo tiene una `imagen_url` opcional dentro de `Diagnostico`.

## Ejercicio 12 — Apps Django por módulo

Se crearon y registraron las apps `core`, `parcelas` y `diagnosticos`, adaptadas al dominio de Ojo d’Chakra. No se crearon `catalogo`, `clientes` ni `pedidos`, porque corresponden a una tienda y no al proyecto integrador. Se conserva `core` como app base del proyecto.

La app `historial` se mantiene registrada para no romper la API funcional: por ahora contiene los modelos `Parcela` y `Diagnostico`, sus serializers, vistas, rutas y pruebas. Las apps `parcelas` y `diagnosticos` recién creadas son esqueletos vacíos; su objetivo es separar esos dominios gradualmente, no duplicar modelos todavía.

```text
src/semana13/backend/
├── manage.py
├── config/
│   ├── settings.py
│   └── urls.py
├── core/                 App base, conservada y registrada
├── parcelas/             App del módulo de parcelas, registrada
├── diagnosticos/         App del módulo de diagnósticos, registrada
└── historial/            API y modelos que siguen activos
```

La configuración `INSTALLED_APPS` está en `src/semana13/backend/config/settings.py` e incluye las apps propias:

```python
'core.apps.CoreConfig',
'parcelas.apps.ParcelasConfig',
'diagnosticos.apps.DiagnosticosConfig',
'historial.apps.HistorialConfig',
```

Desde la carpeta del backend se ejecutó:

```powershell
python manage.py check
```

Salida:

```text
System check identified no issues (0 silenced).
```

`check` confirma que Django carga la configuración y las apps registradas sin errores. No mueve los modelos ni cambia las rutas actuales de `historial`.

## Ejercicio 13 — Estructura React y mapa de rutas

Se reutilizan `components/`, `pages/` y `src/api.js`, que ya están creados. Se agregaron archivos vacíos para las pantallas pendientes de Ojo d’Chakra; `DiagnosticosPage.jsx` se conserva implementada como pantalla de listado. Las páginas todavía vacías se documentan como propuestas y no se agregaron a las rutas activas de `App.jsx`.

```text
src/semana13/frontend/
├── index.html
├── package.json
├── vite.config.js
└── src/
    ├── api.js
    ├── App.jsx
    ├── main.jsx
    ├── components/
    │   └── DiagnosticoCard.jsx
    └── pages/
        ├── DiagnosticosPage.jsx       Implementada: lista de diagnósticos
        ├── ParcelasPage.jsx           Vacía: lista de parcelas
        ├── HistorialParcelaPage.jsx   Vacía: historial de una parcela
        └── DiagnosticoFormPage.jsx    Vacía: crear o editar diagnóstico
```

### Mapa de recursos API y pantallas React

| Recurso / operación | Ruta API de Django (Semana 13: puerto 8002) | Ruta React | Estado de React |
|---|---|---|---|
| Listar parcelas | `GET /api/parcelas/` | `/parcelas` | Propuesta; `ParcelasPage.jsx` está vacía. |
| Consultar historial de una parcela | `GET /api/parcelas/<uuid>/historial/` | `/parcelas/:parcelaId/historial` | Propuesta; `HistorialParcelaPage.jsx` está vacía. |
| Listar diagnósticos y aplicar búsqueda/filtros | `GET /api/diagnosticos/?parcela=<uuid>&search=...&plaga_detectada=...` | `/diagnosticos?parcela=<uuid>&search=...` | La ruta `/diagnosticos` y el listado están implementados; los filtros del frontend están pendientes. |
| Crear diagnóstico | `POST /api/diagnosticos/` | `/diagnosticos/nuevo` | Propuesta; `DiagnosticoFormPage.jsx` está vacía. |
| Consultar, actualizar o eliminar diagnóstico | `GET`, `PATCH` o `DELETE /api/diagnosticos/<uuid>/` | `/diagnosticos/:id/editar` para consulta/edición; eliminar desde la misma pantalla | API implementada; pantalla y acciones React pendientes. |

Las rutas de React son el diseño de navegación; salvo `/diagnosticos`, no están todavía conectadas en `App.jsx`. Las rutas de Django sí están expuestas por la API. Para probarla, el host local es `http://127.0.0.1:8002`, y `api.js` centraliza esa URL base para las peticiones del frontend.

## Carpetas relevantes

```text
src/
├── semana11/
│   ├── backend/
│   │   ├── config/             Proyecto Django y rutas principales
│   │   └── historial/          Modelos, serializers, vistas y rutas REST
│   ├── frontend/               Interfaz de práctica con datos mock
│   └── README.md
├── semana12/
│   ├── frontend/
│   │   └── src/integrador/     Panel React de Ojo d’Chakra
│   └── README.md
└── semana13/
    ├── backend/                Proyecto Django con core, parcelas, diagnosticos e historial
    ├── frontend/               Estructura inicial React y Axios
    └── README.md               Diseño y documentación de esta semana
```

El backend de Semana 13 es una copia independiente para practicar la estructura sin afectar las semanas anteriores; el frontend sigue siendo el de Semana 12.

## Repositorio

[https://github.com/adrienyldefonso-sys/mydjango](https://github.com/adrienyldefonso-sys/mydjango)
