# Semana 12 — Ejercicio 1: verificar la API

## Recurso y petición

- **Recurso:** productos de la óptica.
- **Servidor:** Django de `src/semana8`.
- **URL de la lista:** `http://127.0.0.1:8000/optica-v3/api/productos/`
- **Método:** `GET`
- **Estado verificado en el navegador:** `200 OK`
- **Tipo de contenido:** `application/json`

Para levantar Django desde la raíz del repositorio:

```powershell
cd .\src\semana8
python manage.py runserver 127.0.0.1:8000
```

La ruta `/optica-v3/` incluye las URL de la aplicación `semana5`, y el router de esa aplicación publica el recurso bajo `/api/productos/`. La búsqueda por texto puede probarse con `?search=armazon`.

## Fragmento de la respuesta JSON

```json
[
  {
    "id": 7,
    "nombre": "Armazón Classic",
    "tipo": "armazon",
    "marca": "VisionPro",
    "precio": "240.00",
    "stock": 10
  }
]
```

La lista completa incluye más registros. El fragmento muestra un objeto de esa respuesta.

## Operaciones CRUD

| Operación | Método HTTP | URL | Código de estado esperado |
|---|---|---|---|
| Listar productos | GET | `/optica-v3/api/productos/` | 200 |
| Buscar productos | GET | `/optica-v3/api/productos/?search=armazon` | 200 |
| Consultar un producto | GET | `/optica-v3/api/productos/{id}/` | 200; 404 si no existe |
| Crear un producto | POST | `/optica-v3/api/productos/` | 201; 400 si los datos no son válidos |
| Reemplazar un producto | PUT | `/optica-v3/api/productos/{id}/` | 200; 400 si los datos no son válidos; 404 si no existe |
| Actualizar parcialmente un producto | PATCH | `/optica-v3/api/productos/{id}/` | 200; 400 si los datos no son válidos; 404 si no existe |
| Eliminar un producto | DELETE | `/optica-v3/api/productos/{id}/` | 204; 404 si no existe |

## Diferencia con una respuesta de Template

Un Template de Django normalmente produce una página HTML completa en el servidor, combinando una plantilla con los datos, y el navegador la muestra como una página. En este caso, la API responde con datos JSON y el estado HTTP de la operación. React puede usar esos datos para actualizar solo la parte necesaria de la interfaz, sin solicitar una página HTML completa.

## Implementación existente reutilizada

No se duplicó el proyecto Django ni su base de datos. La Semana 12 consulta el backend existente de Semana 8, para mantener una sola API y una sola fuente de datos:

- [Rutas principales del proyecto](../semana8/config/urls.py)
- [Rutas del API de productos](../semana8/semana5/urls.py)
- [ViewSet de productos y búsqueda](../semana8/semana5/views.py)
- [Serializer y validación de precio](../semana8/semana5/serializers.py)

## Ejercicio 3 — Instalar Axios y crear una instancia

Se creó un frontend independiente en `src/semana12/frontend`. Desde esa carpeta se instaló Axios con:

```powershell
npm install axios
```

### Instancia centralizada: `frontend/src/api.js`

```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/optica-v3/api',
  timeout: 10000,
})

export default api
```

La `baseURL` corresponde a la ruta real de la API de Semana 8. Por ejemplo, para listar productos se podrá usar `api.get('/productos/')`. El tiempo máximo de espera configurado es de 10 segundos.

### Dependencias de `frontend/package.json`

```json
"dependencies": {
  "axios": "^1.21.1",
  "react": "^19.2.8",
  "react-dom": "^19.2.8"
}
```

El archivo completo está en [frontend/package.json](frontend/package.json), y la instancia implementada en [frontend/src/api.js](frontend/src/api.js).

Centralizar la dirección del servidor permite cambiar la URL de la API en un solo lugar. Los componentes pueden reutilizar la instancia `api`, evitando repetir la dirección base y el timeout en cada petición.

## Ejercicio 4 — Solicitud GET con `useEffect`

El componente [ListaPractica.jsx](frontend/src/practica/ListaPractica.jsx) solicita la lista de productos a `GET /productos/`, guarda `respuesta.data` en el estado y la muestra con `map()`. Cada producto usa `producto.id` como `key`. También muestra estados de carga y error.

```jsx
useEffect(() => {
  const cargarProductos = async () => {
    try {
      const respuesta = await api.get('/productos/')
      setProductos(respuesta.data)
    } catch (errorPeticion) {
      console.error('No se pudo cargar la lista.', errorPeticion)
      setError('No se pudo cargar la lista.')
    } finally {
      setCargando(false)
    }
  }

  cargarProductos()
}, [])
```

La petición va en `useEffect` porque es un efecto secundario: comunica el componente con un servidor externo. Si se ejecutara directamente en el cuerpo del componente, cada renderizado volvería a hacer la petición y actualizar el estado provocaría más renderizados y peticiones. El arreglo vacío indica que el efecto se ejecuta al montar el componente.

La función que se pasa a `useEffect` no se declara `async` porque React espera que esa función devuelva `undefined` o una función de limpieza, no una `Promise`. Por eso se declara y llama una función `async` dentro del efecto.

Con Django en `127.0.0.1:8000` y React en `localhost:5173`, la pestaña **Network** debe mostrar una solicitud a `/optica-v3/api/productos/` con método **GET** y estado **200**. La página muestra la lista recibida desde Django.

En modo desarrollo, `main.jsx` usa `StrictMode`, que vuelve a ejecutar los efectos durante el montaje para ayudar a detectar efectos secundarios. Por ello, Network puede mostrar dos solicitudes GET con estado 200; es normal en desarrollo y no indica un fallo de la API.

## Ejercicio 5 — Estados de carga y de error

El componente mantiene tres estados explícitos. Mientras se resuelve la petición muestra `Cargando...`. Si el servidor falla, `catch` registra el error y la página muestra `No se pudo cargar la lista.`. El bloque `finally` desactiva la carga tanto si la petición tuvo éxito como si falló. Si el servidor responde con una lista vacía, la página muestra `No hay productos registrados.`.

Para comprobar el error, se apagó temporalmente Django mientras React seguía activo. La petición no pudo conectarse al servidor; se mostró `No se pudo cargar la lista.`. La consola registró `No se pudo cargar la lista. AxiosError: Network Error`, y Network mostró `GET .../productos/` fallido con `net::ERR_CONNECTION_REFUSED`. En desarrollo puede aparecer dos veces por `StrictMode`. Después de la prueba, Django se volvió a iniciar y el GET volvió a responder 200.

| Estado | Qué ve la persona usuaria |
|---|---|
| Cargando | `Cargando...`, mientras se espera la respuesta. |
| Error | `No se pudo cargar la lista.` si la API no está disponible. |
| Lista vacía | `No hay productos registrados.` si la API responde correctamente sin elementos. |

Estos mensajes evitan dejar una pantalla en blanco: informan si la aplicación está trabajando, si ocurrió un problema o si no hay datos para mostrar, y ayudan a distinguir una lista vacía de una falla de conexión.

## Ejercicio 6 — Solicitud POST con un formulario controlado

El formulario controlado está en [ListaPractica.jsx](frontend/src/practica/ListaPractica.jsx). Cada entrada guarda su valor en `formulario` mediante `value` y `onChange`. Al enviar, se llama `api.post('/productos/', datos)`. Si Django responde correctamente, se agrega `respuesta.data` al estado con un arreglo nuevo:

```jsx
const respuesta = await api.post('/productos/', {
  ...formulario,
  precio: Number(formulario.precio),
  stock: Number(formulario.stock),
})
setProductos((actuales) => [...actuales, respuesta.data])
```

### Prueba válida

Se envió `Producto Semana 12 AJAX`, tipo `armazon`, marca `Laboratorio`, precio `57.90` y stock `2`. Network confirmó **POST 201 Created**. Django devolvió el registro con `id: 25`, y React lo agregó a la lista sin recargar la página.

### Prueba de validación

Se volvió a enviar el formulario con precio `0`. El serializer de Semana 8 rechaza los precios menores o iguales a cero. Network confirmó **POST 400 Bad Request** y la respuesta fue:

```json
{
  "precio": [
    "El precio debe ser mayor que cero."
  ]
}
```

El componente muestra `errorPeticion.response.data` en pantalla como JSON para que la persona usuaria vea la validación del servidor. El registro inválido no se agrega a la lista. Si Network también muestra una solicitud `OPTIONS`, es la comprobación previa de CORS; para documentar el resultado CRUD, selecciona la solicitud `POST`.

## Ejercicio 7 — Solicitudes DELETE y PATCH

Cada producto tiene un botón **Aumentar stock (+1)** y otro **Eliminar**. El primero envía un `PATCH` a `/productos/{id}/` y reemplaza en el estado el producto actualizado mediante `map()`. El segundo envía `DELETE` a la misma ruta y, al recibir el estado `204`, quita el producto del estado con `filter()`. Mientras una operación está en curso, los botones quedan deshabilitados y la interfaz muestra el resultado o el error.

### Pruebas realizadas con el producto de id 25

| Acción | Antes | Solicitud y respuesta | Después |
|---|---|---|---|
| Aumentar stock | `Producto Semana 12 AJAX`, stock `2` | `PATCH /optica-v3/api/productos/25/` — **200 OK**. El JSON devolvió `stock: 3`. | El producto siguió en la lista con stock `3`, sin recargar la página. |
| Eliminar | El mismo producto, stock `3` | `DELETE /optica-v3/api/productos/25/` — **204 No Content**. | El producto desapareció de la lista; los demás registros permanecieron. |

Para documentar la evidencia en el navegador, abre **Network**, selecciona la solicitud `PATCH` o `DELETE` correspondiente y captura el método, la ruta y el código de estado junto con la lista antes o después de la acción. El registro de prueba de id `25` se eliminó al finalizar la comprobación; puedes crear otro con el formulario si necesitas repetir las capturas.

## Ejercicio 8 — Parámetros de búsqueda y verificación

El campo **Buscar productos** es controlado por el estado `buscar`. Cada cambio actualiza ese estado y `useEffect` vuelve a pedir la lista con Axios. La dependencia `[buscar]` hace que el efecto se ejecute al montar el componente y cada vez que cambia el texto:

```jsx
const respuesta = await api.get('/productos/', {
  params: { search: buscar },
})
```

Axios convierte `params` en la cadena de consulta de la URL. La prueba se realizó buscando `VisionPro`; en **Network** se verificó `GET http://127.0.0.1:8000/optica-v3/api/productos/?search=VisionPro`, estado **200**, con el producto `Armazón Classic` en la respuesta. Para la captura, escribe un término en el campo y selecciona el GET correspondiente en Network.

### Recorrido de la petición

1. **React** mantiene el texto de búsqueda en `buscar` y vuelve a dibujar el componente cuando cambia.
2. **Axios** envía el GET a la dirección centralizada y codifica `search` como parámetro de consulta.
3. El **ViewSet** de productos recibe la petición; `SearchFilter` aplica la búsqueda en los campos `nombre`, `marca` y `tipo`.
4. El **serializer** convierte los objetos `Producto` obtenidos en datos JSON para la respuesta.
5. El **ORM** consulta la base de datos y entrega los productos que coinciden con el filtro.
6. React guarda el JSON en el estado y dibuja los resultados, o muestra carga, error o lista vacía.

### Verificación del proyecto

Se añadieron `eslint.config.js` y el script `lint` de `package.json`. Desde `src/semana12/frontend`, se ejecutaron los dos comandos solicitados:

```text
> npm run lint
> eslint .

Sin errores.
```

```text
> npm run build
> vite build
✓ 76 modules transformed.
✓ built in 165ms
```

### Acceso a la API

En este proyecto no se configuraron autenticación ni clases de permisos para la API; Django REST Framework usa por defecto `AllowAny` cuando no se define otra política. Por eso las rutas de productos permiten leer y modificar datos a cualquier cliente que pueda alcanzarlas. `CORS_ALLOWED_ORIGINS` no es autenticación: controla qué orígenes de páginas web pueden leer la respuesta desde un navegador, pero no bloquea clientes como `curl` o Postman. En una aplicación publicada se deben configurar autenticación, permisos y las restricciones adecuadas antes de exponer datos o permitir cambios.

## Parte 2 — Ojo d’Chakra en Semana 12

La Parte 2 está en el mismo frontend de Semana 12, en una sección separada de **Parte 1: práctica**. Así se conservan los ejercicios de productos y el panel integrador sin mezclarlos. La API de este panel es el backend de práctica de Semana 11, en `http://127.0.0.1:8001/api`; el puerto `8001` evita interferir con el servidor de Semana 8 en `8000`.

### Ejercicio 9 — Recurso y operaciones

La entidad principal es **Diagnóstico**, relacionada con una **Parcela**.

| Recurso | URL | Campos | Validación para HTTP 400 | Filtros | Operaciones |
|---|---|---|---|---|---|
| Diagnóstico | `/api/diagnosticos/` | `id`, `parcela`, `fecha_captura`, `plaga_detectada`, `plaga_nombre`, `confianza`, `imagen_url` | `validate_confianza`: de 0 a 100 y hasta 2 decimales; `100.01` responde 400. | `?search=` por nombre/código; `?plaga_detectada=` por código exacto; `?ordering=` por fecha/nombre/código/confianza; `?parcela=<UUID>`; `?desde=YYYY-MM-DD&hasta=YYYY-MM-DD`. | GET/POST en la colección; GET/PUT/PATCH/DELETE en `/api/diagnosticos/<uuid>/`. |

### Ejercicio 10 — GET, carga, error y adaptación

El padre [PanelDiagnosticos.jsx](frontend/src/integrador/PanelDiagnosticos.jsx) carga las parcelas con `GET /api/parcelas/` y luego obtiene la lista desde `GET /api/diagnosticos/?parcela=<uuid>`. El padre guarda la parcela, los diagnósticos y los estados de carga y error; entrega los diagnósticos al listado mediante props. Las funciones adaptadoras convierten `confianza`, `latitud` y `longitud` de texto decimal a número. La instancia [api.js](frontend/src/api.js) conserva la API de productos como predeterminada y exporta `apiOjoChakra` para el backend del integrador.

Se cargaron cinco registros demo con `python manage.py loaddata demo_historial`, porque la base de Semana 11 estaba vacía. En la prueba del navegador, ambos endpoints GET respondieron **200** y se mostraron los cinco diagnósticos de Chacra Los Andes. En desarrollo `StrictMode` puede duplicar las solicitudes. Para entregar la evidencia, captura el panel y el GET del historial con estado 200 en **Network**.

### Ejercicio 11 — Alta y edición

El formulario controlado envía `POST /api/diagnosticos/`. Al recibir **201 Created**, el padre adapta `respuesta.data` y agrega el diagnóstico con un arreglo nuevo. El botón **Editar** selecciona un registro; el formulario se carga con sus valores y el envío realiza `PATCH /api/diagnosticos/<uuid>/`. Al recibir **200 OK**, el padre actualiza ese elemento con `map()`. Las respuestas de validación del serializer se muestran en el formulario.

Pruebas realizadas con la fila `9c7e603e-08e1-41dd-a012-83b161a88b97`:

| Acción | Datos/cambio | Resultado |
|---|---|---|
| Alta | Tizón Temprano, confianza `87.45` | `POST /api/diagnosticos/` respondió **201** y la fila se agregó al listado. |
| Edición | Confianza de `87.45` a `91.25` | `PATCH /api/diagnosticos/9c7e603e-08e1-41dd-a012-83b161a88b97/` respondió **200**; la fila mostró `91.25` y se mantuvo tras recargar. |
| Validación | POST con confianza `100.01` | Respondió **400**; el formulario mostró `{"confianza":["La confianza debe estar entre 0 y 100."]}` y no agregó otra fila. |

Para las capturas del informe, muestra el formulario antes y después de **Crear diagnóstico** y **Guardar cambios**, y en **Network** selecciona las solicitudes POST y PATCH para que se vean sus códigos **201** y **200**. La validación también puede capturarse seleccionando el POST con estado **400**.

Para iniciar el backend desde la raíz del repositorio:

```powershell
cd .\src\semana11\backend
python manage.py runserver 127.0.0.1:8001
```

En otra terminal, inicia el frontend desde `src\semana12\frontend` con `npm run dev`. CORS permite `http://localhost:5173`; el backend de práctica usa `AllowAny`, así que no debe exponerse sin autenticación y permisos en un entorno real.

### Ejercicio 12 — Eliminar con confirmación

En `frontend/src/integrador/PanelDiagnosticos.jsx`, `eliminarDiagnostico` pide confirmación con `window.confirm()` y ejecuta `DELETE /api/diagnosticos/<uuid>/`. Solo con **204 No Content** elimina el registro del estado con `filter()` y muestra el mensaje de éxito. Si la API devuelve **404 Not Found**, conserva el estado local y muestra que el registro ya no existe en el servidor; se puede recargar la página para sincronizarlo. `DiagnosticoCard.jsx` pasa el registro seleccionado al padre y deshabilita su botón mientras la solicitud está en curso.

| Prueba | Resultado verificado |
|---|---|
| Confirmar la eliminación del diagnóstico `9c7e603e-08e1-41dd-a012-83b161a88b97` | `DELETE` a `/api/diagnosticos/9c7e603e-08e1-41dd-a012-83b161a88b97/` respondió **204**; desapareció de la lista, que pasó de seis a cinco registros. |
| Reintentar desde la fila de un registro que ya se había borrado (`36a22d58-7fa3-41f1-9feb-7f0ed79a5476`) | `DELETE` respondió **404**; la fila mostró “El diagnóstico ya no existe en el servidor (HTTP 404). Actualiza la página para sincronizar la lista.” |

Para documentar la evidencia, abre **Network**, filtra por **Fetch/XHR** y limpia las solicitudes. Pulsa **Eliminar**, confirma el diálogo y captura el `DELETE` con estado **204** junto al mensaje y la lista actualizada. Para el **404**, elimina primero el registro desde Thunder Client/Postman sin recargar React; después confirma Eliminar en la fila que quedó visible y captura el `DELETE` con estado **404** y el aviso en pantalla. El diálogo se puede cancelar para comprobar que cancelar no envía la solicitud.

### Ejercicio 13 — Búsqueda, filtro y resumen con datos de la API

El [Buscador.jsx](frontend/src/integrador/components/Buscador.jsx) controla el texto de búsqueda y el filtro exacto por código de plaga. Al cambiar cualquiera de los valores, el `useEffect` de [PanelDiagnosticos.jsx](frontend/src/integrador/PanelDiagnosticos.jsx) cancela la solicitud anterior con `AbortController` y hace un nuevo GET a `/api/diagnosticos/`, enviando `parcela`, `search` y `plaga_detectada` como parámetros. El ViewSet filtra la plaga por igualdad exacta. El resumen se deriva con `reduce()` de los diagnósticos que devolvió la API; por eso el total y los conteos reflejan el resultado actual.

Pruebas realizadas sobre la parcela `0f56200f-4b59-4830-b94a-685c14b0143c`:

| URL generada | Estado y resultado |
|---|---|
| `http://127.0.0.1:8001/api/diagnosticos/?parcela=0f56200f-4b59-4830-b94a-685c14b0143c&search=blight` | **200**; 3 resultados (1 Tizón Temprano y 2 Tizón Tardío); resumen: total 3. |
| `http://127.0.0.1:8001/api/diagnosticos/?parcela=0f56200f-4b59-4830-b94a-685c14b0143c&search=blight&plaga_detectada=Potato___Late_blight` | **200**; 2 resultados, ambos Tizón Tardío; resumen: total 2. |

En **Network**, filtra por **Fetch/XHR**, escribe `blight` en el buscador y captura el GET con total 3. Luego selecciona **Tizón Tardío** y captura el GET combinado, la URL con `&plaga_detectada=...`, estado 200 y resumen total 2.
