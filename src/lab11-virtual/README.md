# Laboratorio 11 virtual — Historial de diagnósticos

Esta carpeta contiene una copia independiente del frontend React de Semana 11.
Permite practicar con los componentes del historial sin modificar
`src/semana11/frontend/`.

## Ejecutar

Desde `frontend/`, ejecuta:

```powershell
npm install
npm run dev
```

Abre la dirección local que muestra Vite. Para comprobar la compilación, ejecuta
`npm run build`; para revisar el código con Oxlint, ejecuta `npm run lint`.

## Repositorio y descripción de la pantalla

Repositorio: [https://github.com/adrienyldefonso-sys/mydjango](https://github.com/adrienyldefonso-sys/mydjango).

La pantalla del panel comienza con el encabezado «Ojo d’Chakra» y los datos de
la parcela Chacra Los Andes. Debajo se encuentran el buscador y el formulario
para registrar diagnósticos; el resumen muestra el total y los conteos por
plaga, junto al listado de filas con fecha, confianza y acciones. Al final se
muestra el carrito de diagnósticos seleccionados con sus unidades y la suma de
confianza, no un monto monetario.

## Flujo de datos entre componentes

`PanelDiagnosticos` conserva el estado compartido porque el formulario, el
buscador, el listado, el resumen y el carrito dependen de los mismos datos.
Desde ese padre bajan por props la parcela y el callback `onGuardar` al
formulario, el valor de búsqueda y su función de cambio al buscador, la lista
filtrada y las funciones de acción a cada fila, y las líneas y funciones de
quitar o vaciar al carrito. El resumen recibe por props valores derivados del
arreglo, sin guardarlos en otro estado. En sentido inverso, los hijos avisan al
padre con funciones: el formulario envía el diagnóstico nuevo, el buscador
comunica el texto, cada fila comunica agregar/eliminar/cambiar estado y el
carrito comunica quitar o vaciar. Así el padre actualiza el estado de forma
inmutable y mantiene sincronizados el listado, el filtro y el resumen sin que
los hijos modifiquen directamente las props.

## Comunicación entre componentes

- `App` es el punto de entrada y renderiza `PanelDiagnosticos`.
- `PanelDiagnosticos` mantiene en `useState` los cinco diagnósticos de ejemplo,
  el texto de búsqueda, el carrito y el aviso; comparte datos y callbacks.
- `HistorialParcela` recibe la parcela, el resumen derivado y el callback para
  agregar un diagnóstico; contiene el formulario y el listado.
- `DiagnosticoForm` valida los campos y envía el diagnóstico nuevo al padre
  mediante `onGuardar`.
- `ResumenDiagnosticos` muestra el total y los conteos agrupados por código de plaga.
- `Buscador` recibe el texto y el callback para cambiarlo; el input es controlado.
- `PanelDiagnosticos` filtra los diagnósticos por nombre o código antes de
  pasarlos a `DiagnosticoLista`.
- `DiagnosticoLista` usa `map()` y una `key` basada en el id para crear cada fila.
- `DiagnosticoLista` muestra los diagnósticos filtrados o el mensaje cuando no
  hay coincidencias.
- `DiagnosticoCard` muestra cada diagnóstico y mantiene el estado local para
  mostrar u ocultar su imagen.
- `mockHistorial.js` contiene cinco registros con la forma de la respuesta
  simulada; la confianza y las coordenadas decimales están como texto.
- `index.css` contiene los estilos de la interfaz y sus componentes.
- `PanelDiagnosticos` pasa `agregarAlCarrito` a `DiagnosticoLista`, que la reenvía
  a cada `DiagnosticoCard` como `onAgregar`.
- `Carrito` es hermano de la lista de parcelas y recibe las líneas del carrito
  mediante props. Cada línea usa el id, nombre y confianza de un diagnóstico,
  además de la cantidad de veces que se agregó; no se muestra precio porque los
  datos del proyecto no incluyen ese campo.

El estado del carrito vive en `PanelDiagnosticos`, el padre común. Si estuviera dentro de
`DiagnosticoCard` o `DiagnosticoLista`, quedaría aislado en esos componentes y
`Carrito` no podría recibir de forma consistente las selecciones hechas en las
tarjetas. Al mantenerlo en `PanelDiagnosticos`, la función actualiza el estado
de forma inmutable y React entrega las líneas actualizadas a `Carrito`.

## Ejercicio 10: panel y cinco registros

`PanelDiagnosticos.jsx` es el padre de la pantalla y guarda directamente el
arreglo de cinco diagnósticos en su estado. Cada registro conserva los campos
`id`, `fecha_captura`, `plaga_detectada`, `plaga_nombre`, `confianza` e
`imagen_url`; `confianza` está serializada como texto decimal, por ejemplo
`"98.50"`. Las coordenadas de la parcela también se representan como texto.
Los valores se convierten a número solo cuando se realizan cálculos o se
formatean para mostrarlos.

El padre calcula el resumen desde el mismo arreglo: cantidad de registros,
fecha más reciente y conteo por plaga. Así, al agregar un diagnóstico desde el
formulario, el listado y el resumen se actualizan juntos sin mantener otro
estado duplicado.

## Ejercicio 11: acciones del listado

Cada `DiagnosticoCard` muestra las acciones «Desactivar»/«Activar» y «Eliminar».
La fila no modifica la lista: avisa al padre con `onCambiarEstado(id)` o
`onEliminar(id)`. `DiagnosticoLista` reenvía esas funciones por props y
`PanelDiagnosticos` actualiza el estado de forma inmutable: usa `map()` para
cambiar `activo` y `filter()` para eliminar el registro. Si se elimina un
diagnóstico que está en el carrito, el padre también quita su línea con
`filter()`. No se usa `push()` ni `splice()` sobre el estado.

La propiedad `activo` es solo un indicador local del ejercicio: se inicializa
en `true` para los cinco registros y también para los diagnósticos nuevos; no
se presenta como un campo recibido de la API. El resumen sigue contando todos
los diagnósticos, estén activos o inactivos.

Antes de probar las acciones, el listado tiene cinco filas, todas activas y en
este orden: Saludable, Tizón Tardío, Tizón Temprano, Tizón Tardío y Saludable.
Al desactivar la primera fila, siguen siendo cinco en el mismo orden, pero esa
fila muestra «Inactivo» y el botón cambia a «Activar». Al volver a activarla,
la fila muestra «Activo». Al eliminar esa primera fila, quedan cuatro en el
orden original: Tizón Tardío, Tizón Temprano, Tizón Tardío y Saludable; el
resumen también pasa de cinco a cuatro registros. Estos cambios se reflejan al
volver a renderizar el panel.

## Ejercicio 12: formulario controlado y validación

`DiagnosticoForm.jsx` conserva en estado cada valor del formulario y valida
antes de invocar `onGuardar`. Exige seleccionar un diagnóstico, una fecha
válida y una confianza entre 0 y 100 con hasta dos decimales, de acuerdo con
las reglas del modelo de diagnósticos. La URL de imagen es opcional; si se
ingresa, debe ser HTTP o HTTPS. `noValidate` permite que el formulario muestre
los errores definidos por React. Si todos los datos son válidos, el formulario
envía el objeto al padre; `PanelDiagnosticos.jsx` lo agrega con un arreglo nuevo
y luego se limpian los campos.

Prueba válida: selecciona «Tizón Tardío», ingresa una fecha y hora, y escribe
`92.10` como confianza. Al guardar, el registro aparece al inicio del listado,
el resumen se actualiza, aparece el mensaje de éxito y los campos quedan vacíos.

Prueba inválida: ingresa `100.01` como confianza y completa los demás campos.
El formulario muestra «La confianza debe ser un número entre 0 y 100, con
máximo dos decimales», no llama a `onGuardar` y conserva los valores para que
puedan corregirse.

## Ejercicio 13: resumen, búsqueda y efectos

`PanelDiagnosticos.jsx` calcula el total, la fecha más reciente y el conteo por
plaga con `reduce()` directamente desde `diagnosticos`; no crea otro `useState`
para esos datos. `ResumenDiagnosticos` recibe el total y el conteo por props y
es hermano de `DiagnosticoLista` dentro de `resumen-y-lista`. Por eso el resumen
y las filas se actualizan con el mismo estado del padre al agregar o eliminar
un registro.

`Buscador` es un input controlado: su valor y `onCambiar` vienen del padre.
`PanelDiagnosticos` filtra con `filter()` e `includes()` por nombre o código y
entrega el resultado a `DiagnosticoLista`. En la pantalla inicial hay cinco
registros: Saludable 2, Tizón Tardío 2 y Tizón Temprano 1. Buscar `Tizón`
muestra tres filas; buscar `zzz` deja cero y muestra «No hay diagnósticos que
coincidan». Después de un alta válida de Tizón Tardío, el resumen muestra seis
registros: Saludable 2, Tizón Tardío 3 y Tizón Temprano 1.

`Carrito.jsx` usa `useEffect` con `[unidades]` para actualizar el título de la
pestaña cuando cambia la cantidad seleccionada; por ejemplo,
`Carrito (1) — Diagnósticos`. Su limpieza restaura el título anterior.
`Aviso.jsx` también usa un efecto: muestra «Agregado: <nombre>» durante tres
segundos y limpia el temporizador si el aviso cambia o el componente se
desmonta. La pantalla muestra ese aviso al agregar una fila al carrito.

## Datos derivados del carrito

En `Carrito`, `reduce()` calcula las unidades y la suma de confianza a partir de
las líneas recibidas; esos resultados no se guardan en otro estado. Al agregar
dos veces «Saludable» (98.50) y una vez «Tizón Tardío» (92.10), el resultado es
3 unidades y 289.10 puntos de confianza. No es un total monetario porque los
diagnósticos no tienen precio.

El total no necesita `useState`: se deriva de `lineas` y se vuelve a calcular
cuando React renderiza el componente con las líneas actualizadas. Guardarlo
también como estado duplicaría información y podría desincronizarse.

## Búsqueda compartida

`Buscador` y `DiagnosticoLista` no se comunican directamente: ambos reciben
props de `PanelDiagnosticos`, que es el padre común. `Buscador` avisa al padre cuando cambia el
texto; `PanelDiagnosticos` filtra los diagnósticos con `filter()` e `includes()` y pasa el
resultado a `DiagnosticoLista`. Con estos datos, buscar `ca` o `zzz` no encuentra
diagnósticos y se muestra «No hay diagnósticos que coincidan».

Cada línea de `Carrito` ofrece «Quitar», que avisa a `PanelDiagnosticos` mediante `onQuitar(id)`;
el padre elimina esa línea con `filter()`. «Vaciar carrito» avisa mediante
`onVaciar` y el padre reemplaza el estado por un arreglo vacío. Cuando no hay
líneas, el mensaje «El carrito está vacío» se muestra con `&&`.

En `DiagnosticoCard`, el evento se enlaza con
`onClick={() => onAgregar(diagnostico)}` para que el callback se ejecute al
pulsar el botón. La prueba temporal del ejercicio anterior usó
`onClick={onAgregar(diagnostico)}` cuando el callback solo imprimía en consola:
el mensaje aparecía durante el renderizado (posiblemente varias veces por
`StrictMode`) y el clic no generaba otro mensaje. Ahora que el callback también
actualiza el carrito, esa expresión ejecutaría la actualización de estado
durante el render de `DiagnosticoCard`, en vez de esperar el clic, y puede
provocar advertencias o renderizados repetidos. En este proyecto no existe un
campo `stock`, así que no se aplica la condición de desactivar el botón por
stock agotado.

Para documentar la prueba temporal anterior, captura el código incorrecto en
`DiagnosticoCard.jsx` junto con la pestaña **Consola** del navegador mostrando
los mensajes al recargar, antes de pulsar «Agregar». Después restaura la función
flecha correcta.

Agrega al documento Word capturas del código de los componentes, la interfaz en
el navegador y la terminal con los comandos ejecutados.

## Efectos y limpieza

`Carrito` calcula las unidades desde sus props y usa `useEffect` con
`[unidades]` para cambiar el título a `Carrito (n) — Diagnósticos` y registrar
el cambio en la consola. El efecto restaura el título anterior al limpiarse.
`Aviso` muestra el diagnóstico agregado durante tres segundos; su efecto crea
un `setTimeout` y devuelve una limpieza con `clearTimeout`, que cancela el
temporizador anterior si cambia el aviso o se desmonta el componente.

Con `[]`, un efecto se ejecuta al montar (y la limpieza al desmontar); con
`[unidades]`, se ejecuta al montar y cuando cambia ese valor; sin arreglo de
dependencias, se ejecuta después de cada render. En desarrollo,
`React.StrictMode` ejecuta un ciclo adicional de configuración y limpieza al
montar para ayudar a detectar efectos sin limpieza, por lo que el `console.log`
puede aparecer dos veces.

Este proyecto usa diagnósticos, no productos de cafetería; por eso el título
identifica el carrito como «Diagnósticos».

## Verificación del ejercicio 8

`npm run lint` ejecuta `oxlint src` y `npm run build` compila el frontend.
Ambos comandos finalizaron correctamente: Oxlint terminó sin reportar errores
(código de salida 0) y Vite compiló 26 módulos y mostró `built successfully`.

## Verificación final y entrega

- La consola del navegador no mostró advertencias ni errores al cargar y usar
  el panel; en particular, no aparecieron advertencias de `key` en el listado.
- `npm run lint`: finalizó con código 0 y sin errores de Oxlint.
- `npm run build`: Vite compiló 26 módulos y terminó correctamente.
- `frontend/.gitignore` excluye `node_modules/` y `dist/`; `git ls-files` no
  encontró ninguno de esos directorios entre los archivos rastreados.

En el navegador, el título inicial es `Carrito (0) — Diagnósticos`; después
de agregar «Saludable» cambia a `Carrito (1) — Diagnósticos`, y el aviso
`Agregado: Saludable` programa su desaparición a los tres segundos. En la
verificación con una pestaña en segundo plano, el navegador retrasó el
temporizador por throttling, pero el aviso desapareció al esperar más. El
registro inicial del efecto aparece dos veces en desarrollo porque la
aplicación está envuelta en `React.StrictMode`.
