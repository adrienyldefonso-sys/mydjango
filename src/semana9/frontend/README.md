# Semana 9 — Ejercicios 3 y 4: props, listas y children

## Componentes

- `src/components/ProductoItem.jsx` representa un producto. Recibe `nombre`, `precio`, `stock` y `marca` como props desestructuradas. `marca` tiene el valor predeterminado `Marca no especificada`.
- `src/components/ProductoLista.jsx` recibe el arreglo `productos`, lo recorre con `map()` y crea un `ProductoItem` por producto. Usa `producto.id` como `key` estable.
- `src/components/Tarjeta.jsx` es un contenedor reutilizable que recibe `titulo` y `children`, y presenta su contenido dentro de una sección con estilo.
- `src/App.jsx` importa `ProductoLista` y le pasa los datos desde `src/datos.js`.

El nombre `ProductoItem` comienza con mayúscula para que React lo reconozca como componente. El valor predeterminado de `marca` se usa si una llamada no proporciona esa prop.

## Ejercicio 4: contenedor con `children`

En `App.jsx`, la lista se coloca entre las etiquetas de `Tarjeta`:

```jsx
<Tarjeta titulo="Productos">
  <ProductoLista productos={productos} />
</Tarjeta>
```

`Tarjeta` muestra el título y renderiza `{children}` en su interior. Así, puede envolver diferentes secciones sin tener que conocer de antemano el contenido que recibirá.

En Django, el concepto más parecido es un bloque de plantilla como `{% block content %}`: ambos permiten insertar contenido dentro de una estructura contenedora. No son exactamente lo mismo: `children` recibe elementos React desde el componente padre, mientras que los bloques Django forman parte de la composición/herencia de plantillas procesadas en el servidor.

## Ejercicio 5: relación 1:N (cliente y ventas)

- `src/components/ClienteCard.jsx` representa un cliente y recorre su arreglo de ventas.
- `src/components/VentaItem.jsx` representa cada venta relacionada con ese cliente.
- El total se calcula en JavaScript con `reduce()`: precio unitario multiplicado por cantidad para cada venta.
- La API usa `precio_unitario`; al pasar el dato al componente lo convertimos a la prop `precioUnitario`, que sigue la convención camelCase habitual en JavaScript.

Las props son entradas que pertenecen al componente padre. Un componente hijo no debe modificarlas: si necesita cambiar información, debe avisar al padre mediante una función callback. Cambiarlas directamente puede alterar datos compartidos sin que React lo sepa y provocar una interfaz inconsistente. En desarrollo, React congela el objeto superior de props del elemento; una asignación directa como `props.titulo = 'Otro'` puede lanzar un `TypeError` indicando que no se puede asignar a una propiedad de solo lectura. Los objetos anidados no necesariamente están congelados, así que tampoco deben modificarse.

## Ejercicio 6: estado local y evento de clic

`ProductoItem` tiene un estado `revisiones` inicializado en cero mediante `useState`. El botón incrementa ese estado con `setRevisiones`; el mensaje aparece únicamente cuando el contador es mayor que cero. El botón está desactivado cuando el producto está agotado (`stock === 0`). Como cada producto se renderiza como una instancia propia de `ProductoItem`, cada instancia tiene su propio contador.

Una variable normal (`let`) no actualiza la pantalla: React no observa sus asignaciones y no vuelve a renderizar el componente cuando cambia. El setter de `useState`, en cambio, notifica a React que debe renderizar de nuevo con el valor actualizado.

## Ejercicio 7: búsqueda controlada

En `ProductoLista`, el input usa `value={busqueda}` y `onChange` actualiza el estado con `e.target.value`. La lista filtrada compara los nombres en minúsculas, así que la búsqueda no distingue mayúsculas. Si no hay coincidencias, muestra un mensaje.

Pruebas en el navegador:

- Buscar `LENTE` muestra Lente Daily, Lente Daily Flex y Lente Pro.
- Buscar `daily` muestra Lente Daily y Lente Daily Flex.

## Ejercicio 8: formulario controlado

`src/components/ProductoForm.jsx` controla nombre, tipo, marca, precio y stock con `useState`. Al enviar, usa `preventDefault()` y valida que el precio sea mayor que cero, como `ProductoSerializer.validate_precio` en `src/semana8/semana5/serializers.py`. Si la validación falla, muestra un error; si pasa, llama al padre y limpia los campos.

`App.jsx` carga los productos con `GET` y los agrega al estado después de que Django confirma el `POST`. `vite.config.js` configura un proxy `/django-api` al servidor Django para evitar problemas de CORS durante el desarrollo. El formulario solo limpia los campos después de una respuesta exitosa; los errores del servidor se muestran en el formulario.

La persistencia la realiza Django REST Framework mediante `ProductoViewSet` y `ProductoSerializer`; el estado de React solo refleja la respuesta. En producción hay que configurar el origen de API y la autenticación apropiados, en vez de depender del proxy de desarrollo.

Validación ejecutada para este ejercicio: `npm run lint` y `npm run build`; ambas finalizaron correctamente. Para la evidencia, abre las herramientas de desarrollador del navegador, pestaña **Network**, envía el formulario y muestra la petición `POST` con respuesta `201`; luego recarga y verifica que el producto siga apareciendo por el `GET`.

## Resultado esperado

Al ejecutar `npm run dev`, la sección **Productos** muestra un campo para filtrar los registros por nombre, sin distinguir mayúsculas y minúsculas. Cada producto presenta nombre, marca, precio y stock; los productos con stock igual o menor que 10 también muestran **¡Últimas unidades!**. El botón **Registrar revisión** incrementa el contador solo del producto pulsado; no está disponible para un producto agotado. La sección **Ventas por cliente** muestra cada venta como componente anidado y el total calculado para cada cliente (Ana: S/ 600.00; Luis: S/ 240.00).

## Ejecutar y validar

```sh
npm run dev
npm run build
npm run lint
```

---

# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some Oxlint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the Oxlint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and Oxlint's TypeScript related rules in your project.
