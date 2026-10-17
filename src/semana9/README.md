# Semana 9 — Interfaz React para la aplicación de óptica

## Repositorio

Proyecto completo: [https://github.com/adrienyldefonso-sys/mydjango](https://github.com/adrienyldefonso-sys/mydjango)

El proyecto de React con Vite se encuentra en la carpeta [`frontend`](../../frontend) de la raíz del repositorio. No se creó otra copia del frontend dentro de `src/semana9`.

## Requisitos

- Node.js (versión LTS recomendada)
- npm, incluido con Node.js

## Instalar y ejecutar

Desde la raíz del repositorio, ejecuta los siguientes comandos en PowerShell:

```powershell
cd .\frontend
npm install
npm run dev
```

Abre en el navegador la dirección que Vite muestre en la terminal, normalmente [http://localhost:5173/](http://localhost:5173/).

## ¿Qué muestra la interfaz?

La interfaz está construida con React y contiene datos escritos manualmente con una estructura similar a las respuestas JSON de la API desarrollada en la Semana 8. En esta etapa no realiza peticiones al backend.

- Una lista de productos con nombre, tipo, marca, precio y stock.
- Mensajes condicionales para productos agotados o con pocas unidades.
- Una lista de clientes y sus ventas anidadas, con datos del producto, cantidad, fecha y estado.
- El número de ventas y el total de cada cliente, calculados con JavaScript.
- Estilos propios mediante clases CSS y estilos en línea.

## Verificaciones

Desde `frontend`, se pueden ejecutar:

```powershell
npm run lint
npm run build
```

Las carpetas `node_modules` y `dist` están excluidas del control de versiones mediante `frontend/.gitignore`; se generan o instalan localmente cuando se ejecuta el proyecto.
