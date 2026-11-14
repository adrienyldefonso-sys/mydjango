# Semana 11 — Historial de diagnósticos de Ojo d'Chakra

Este laboratorio es independiente del proyecto integrador. El backend de práctica está en `backend/` y el frontend React/Vite está en `frontend/`; no comparten base de datos ni configuración.

## Entidades

- `Parcela`: UUID, nombre, cultivo, referencia, coordenadas y nombre del agricultor.
- `Diagnostico`: UUID, parcela relacionada, fecha, código y nombre de plaga, confianza e imagen opcional.
- Relación: una parcela tiene muchos diagnósticos (`Parcela.diagnosticos`).
- `total_diagnosticos` se calcula desde la relación; no se almacena para evitar que quede desactualizado. El resumen por plaga y la última fecha también se derivarán de los diagnósticos.

Los campos corresponden al mock del historial compartido. La confianza se valida entre 0 y 100; las coordenadas se validan en los rangos geográficos.

## Componentes del Ejercicio 10

- `DiagnosticoCard`: muestra un registro individual, recibe `diagnostico` por props y `mostrarFecha` tiene valor predeterminado.
- `DiagnosticoLista`: recibe un arreglo, lo recorre con `map()` y usa el UUID del diagnóstico como `key`.
- `HistorialParcela`: presenta la parcela y su resumen; recibe `children` para insertar la lista anidada.
- `App`: recorre las parcelas con `map()` y asigna la key con el UUID de parcela.

El frontend usa el mock compartido en `frontend/src/data/mockHistorial.js`. El total del resumen es seis y el ejemplo incluye tres diagnósticos recientes; la lista representa esa muestra parcial, no los seis registros.

## Ejercicio 11: estado y búsqueda

- Antes de pulsar **Ver imagen**, cada tarjeta muestra sus datos y mantiene la imagen oculta. Después del clic, solo esa tarjeta muestra su imagen y el botón cambia a **Ocultar imagen**; un segundo clic la vuelve a ocultar.
- Antes de escribir en **Buscar diagnóstico**, se muestran los tres registros de ejemplo. Buscar `TARDÍO` deja **Tizón Tardío**; buscar `Potato___healthy` deja **Saludable**. La búsqueda ignora mayúsculas y sirve tanto para el nombre como para el código de plaga.
- Si la búsqueda no coincide, se muestra “No hay diagnósticos que coincidan con la búsqueda.”

## Ejercicio 12: relación anidada y formulario

`HistorialParcela` contiene el formulario y `DiagnosticoLista`; cada diagnóstico se representa con `DiagnosticoCard`. `App` conserva las parcelas en estado y pasa un callback al formulario para agregar el registro a la parcela correspondiente, usando arreglos nuevos.

El formulario usa `onSubmit` y `preventDefault()`. Valida fecha/hora, confianza entre 0 y 100 y URL cuando se ingresa una imagen. Envío válido de ejemplo: elegir **Tizón Tardío**, fecha `2026-11-03T10:00`, confianza `91.25` y pulsar **Agregar al historial**; aparece una nueva tarjeta, aumenta el resumen y se limpian fecha y confianza. Envío inválido: confianza `120`; aparece el error “La confianza debe estar entre 0 y 100.” y no se modifica la lista.

Este ejercicio agrega el registro solo al estado React de prueba; no hace una petición a Django y los datos se pierden al recargar.

## Ejercicio 13: verificación de la interfaz

- En el navegador se muestran los tres diagnósticos iniciales; la búsqueda `TIZÓN` devuelve dos coincidencias (Tizón Temprano y Tizón Tardío).
- Se intentó enviar confianza `120`: aparece la validación y la lista conserva sus tres registros.
- Después de recargar la interfaz y realizar estas interacciones, la consola del navegador no mostró advertencias, errores de consola ni errores de ejecución.
- `npm run lint`: completado correctamente (`oxlint src`, sin hallazgos).
- `npm run build`: completado correctamente; Vite transformó 21 módulos y generó `dist/`.
- `node_modules/` y `dist/` están ignorados por `frontend/.gitignore`; `git ls-files` no los reporta, por lo que no forman parte de los archivos rastreados.

## Serializer y reglas de validación

`backend/historial/serializers.py` expone las parcelas, diagnósticos y el historial anidado con la forma del mock. La validación `validate_confianza` exige valores entre 0 y 100 con hasta dos decimales; el modelo también valida los rangos geográficos de la parcela.

- latitud entre -90 y 90 y longitud entre -180 y 180;
- campos textuales obligatorios no vacíos;
- fecha válida y, si se envía, URL de imagen válida.

La API de práctica incluye `GET /api/parcelas/`, `GET /api/parcelas/<uuid>/historial/` y el CRUD de diagnósticos bajo `/api/diagnosticos/`. La colección permite GET, POST, PUT, PATCH y DELETE mediante `DiagnosticoViewSet`; admite `?search=` por nombre/código, `?ordering=` por fecha/nombre/código/confianza, `?parcela=<uuid>` y filtros de fecha `?desde=YYYY-MM-DD&hasta=YYYY-MM-DD`. El historial anidado también conserva los filtros de fecha. Las fechas mal formadas, los rangos invertidos, UUID de parcela inválidos y confianza fuera del rango responden con HTTP 400.

El frontend de Semana 12 (`src/semana12/frontend`) consume el historial de la primera parcela mediante los endpoints anteriores y la instancia Axios `apiOjoChakra`. Para datos de demostración se incluye `historial/fixtures/demo_historial.json`. `django-cors-headers` permite los orígenes de desarrollo `localhost:5173` y `localhost:5174`; el acceso DRF sigue en `AllowAny` para el laboratorio, por lo que la API no debe exponerse sin autenticación y permisos en un entorno real. El frontend `src/lab11-virtual` conserva los datos mock de Semana 11.

La tabla de planificación queda así:

| Necesidad | Componente/validación |
|---|---|
| Mostrar un diagnóstico | `DiagnosticoCard` |
| Botón con estado | `DiagnosticoCard` muestra u oculta la imagen |
| Mostrar la relación parcela-diagnósticos | `HistorialParcela` contiene `DiagnosticoLista` |
| Formulario y regla | `DiagnosticoForm`; valida que la confianza esté entre 0 y 100 |
| Regla de la API | `confianza` debe estar entre 0 y 100; coordenadas también se validan por rango |

## Ejercicio 14: publicación y ejecución del frontend

Repositorio: [https://github.com/adrienyldefonso-sys/mydjango](https://github.com/adrienyldefonso-sys/mydjango).

Para ejecutar el frontend de este laboratorio, abre una terminal en `src/semana11/frontend/` y ejecuta:

```powershell
npm install
npm run dev
```

Vite mostrará la dirección local en la terminal. Para compilar y revisar el código usa `npm run build` y `npm run lint`. El servidor no se inicia automáticamente.

Las carpetas generadas `node_modules/` y `dist/` están excluidas mediante `.gitignore` y no se publican en el repositorio.

## Comprobaciones

Desde `backend/`, instalar dependencias y ejecutar:

```powershell
py -m pip install -r requirements.txt
py manage.py makemigrations historial
py manage.py migrate
py manage.py check
py manage.py test historial
```
