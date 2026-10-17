// Datos de ejemplo con los mismos campos y tipos que devuelve la API de productos.
// Los precios se guardan como texto para coincidir con la respuesta JSON de Django.
const productos = [
  { id: 7, nombre: 'Armazón Classic', tipo: 'armazon', marca: 'VisionPro', precio: '245.00', stock: 10 },
  { id: 9, nombre: 'Armazón Sport', tipo: 'armazon', marca: 'ActiveFit', precio: '260.00', stock: 7 },
  { id: 8, nombre: 'Lente Daily', tipo: 'lente_contacto', marca: 'ClearView', precio: '120.00', stock: 18 },
  { id: 12, nombre: 'Lente Daily Flex', tipo: 'lente_contacto', marca: 'Acuvue', precio: '60.00', stock: 40 },
  { id: 18, nombre: 'Lente Pro', tipo: 'luna', marca: 'Opti', precio: '150.00', stock: 12 },
]

// Ejemplo de relación 1:N: cada cliente contiene varias ventas.
// Las ventas conservan cantidad y precio_unitario, como en el modelo intermedio.
const clientesConVentas = [
  {
    id: 6,
    nombres: 'Ana',
    apellidos: 'García',
    ventas: [
      { id: 12, producto: 'Luna Blue', cantidad: 2, precio_unitario: '180.00' },
      { id: 13, producto: 'Armazón Classic', cantidad: 1, precio_unitario: '240.00' },
    ],
  },
  {
    id: 7,
    nombres: 'Luis',
    apellidos: 'Pérez',
    ventas: [
      { id: 10, producto: 'Lente Daily', cantidad: 2, precio_unitario: '120.00' },
    ],
  },
]

// Datos manuales de la investigación propia con la misma forma que la API de Semana 8.
// Producto devuelve precio como texto y stock como número.
const productosInvestigacion = [
  { id: 7, nombre: 'Armazón Classic', tipo: 'armazon', marca: 'VisionPro', precio: '240.00', stock: 10 },
  { id: 9, nombre: 'Armazón Sport', tipo: 'armazon', marca: 'ActiveFit', precio: '260.00', stock: 7 },
  { id: 8, nombre: 'Lente Daily', tipo: 'lente_contacto', marca: 'ClearView', precio: '120.00', stock: 18 },
  { id: 12, nombre: 'Lente Daily Flex', tipo: 'lente_contacto', marca: 'Acuvue', precio: '60.00', stock: 40 },
  { id: 18, nombre: 'Lente Pro', tipo: 'luna', marca: 'Opti', precio: '150.00', stock: 12 },
]

// Cliente sigue la estructura JSON del serializer: incluye productos como lista de IDs.
const clientesInvestigacion = [
  {
    id: 16, nombres: 'Prueba', apellidos: 'Caso', dni: '99999999Z',
    telefono: '111', fecha_nacimiento: '1990-01-01', productos: [14],
    ventas: [
      {
        id: 101, producto: { id: 7, nombre: 'Armazón Classic', tipo: 'armazon', marca: 'VisionPro', precio: '240.00' },
        fecha_venta: '2025-05-12', cantidad: 1, precio_unitario: '240.00', estado: 'pagado',
      },
      {
        id: 102, producto: { id: 8, nombre: 'Lente Daily', tipo: 'lente_contacto', marca: 'ClearView', precio: '120.00' },
        fecha_venta: '2025-05-15', cantidad: 2, precio_unitario: '120.00', estado: 'entregado',
      },
    ],
  },
  {
    id: 15, nombres: 'Sofía', apellidos: 'Díaz', dni: '50505050E',
    telefono: '600555555', fecha_nacimiento: '2001-01-08', productos: [11],
    ventas: [
      {
        id: 103, producto: { id: 9, nombre: 'Armazón Sport', tipo: 'armazon', marca: 'ActiveFit', precio: '260.00' },
        fecha_venta: '2025-05-18', cantidad: 1, precio_unitario: '260.00', estado: 'pendiente',
      },
    ],
  },
  {
    id: 6, nombres: 'Ana', apellidos: 'García', dni: '11111111',
    telefono: '999111001', fecha_nacimiento: '1990-03-12', productos: [9, 6, 6],
    ventas: [
      {
        id: 104, producto: { id: 12, nombre: 'Lente Daily Flex', tipo: 'lente_contacto', marca: 'Acuvue', precio: '60.00' },
        fecha_venta: '2025-05-20', cantidad: 3, precio_unitario: '60.00', estado: 'pagado',
      },
    ],
  },
  {
    id: 12, nombres: 'Luis', apellidos: 'Gómez', dni: '20202020B',
    telefono: '600222222', fecha_nacimiento: '1988-05-22', productos: [9, 11],
    ventas: [
      {
        id: 105, producto: { id: 18, nombre: 'Lente Pro', tipo: 'luna', marca: 'Opti', precio: '150.00' },
        fecha_venta: '2025-05-22', cantidad: 2, precio_unitario: '150.00', estado: 'entregado',
      },
    ],
  },
  {
    id: 11, nombres: 'Ana', apellidos: 'López', dni: '10101010A',
    telefono: '600111111', fecha_nacimiento: '1990-02-12', productos: [7, 12],
    ventas: [
      {
        id: 106, producto: { id: 7, nombre: 'Armazón Classic', tipo: 'armazon', marca: 'VisionPro', precio: '240.00' },
        fecha_venta: '2025-05-25', cantidad: 1, precio_unitario: '240.00', estado: 'pendiente',
      },
      {
        id: 107, producto: { id: 12, nombre: 'Lente Daily Flex', tipo: 'lente_contacto', marca: 'Acuvue', precio: '60.00' },
        fecha_venta: '2025-05-28', cantidad: 2, precio_unitario: '60.00', estado: 'pagado',
      },
    ],
  },
]

// El componente recorre los productos y crea una fila de interfaz para cada uno.
function App() {
  return (
    <main className="page">
      <h1 className="page-title">Sistema de Óptica</h1>
      <h2 className="section-title">Productos</h2>
      <ul className="product-list">
        {productos.map((producto) => (
          // La key basada en id ayuda a React a identificar cada elemento de la lista.
          <li className="product-item" key={producto.id}>
            {producto.nombre} ({producto.marca}) — S/ {Number(producto.precio).toFixed(2)} —{' '}
            {producto.stock === 0 ? 'Agotado' : `Stock: ${producto.stock}`}
            {producto.stock > 0 && producto.stock <= 10 && (
              <strong className="low-stock"> — ¡Últimas unidades!</strong>
            )}
          </li>
        ))}
      </ul>
      {/* El mensaje aparece solo cuando el arreglo no contiene registros. */}
      {productos.length === 0 && <p className="empty-message">No hay registros</p>}

      <h2 className="section-title">Ventas por cliente</h2>
      {clientesConVentas.map((cliente) => {
        // Sumamos cantidad por precio unitario para obtener el total del cliente.
        const totalCliente = cliente.ventas.reduce(
          (total, venta) => total + Number(venta.precio_unitario) * venta.cantidad,
          0,
        )

        return (
          <section className="customer-card" key={cliente.id}>
            <h3 className="customer-name">{cliente.nombres} {cliente.apellidos}</h3>
            <ul className="sale-list">
              {cliente.ventas.map((venta) => (
                // Cada venta usa su propio id como key dentro de la lista anidada.
                <li className="sale-item" key={venta.id}>
                  {venta.producto} — {venta.cantidad} unidad(es) x S/ {Number(venta.precio_unitario).toFixed(2)}
                </li>
              ))}
            </ul>
            <p className="customer-total" style={{ color: '#176b45' }}>
              Total del cliente: S/ {totalCliente.toFixed(2)}
            </p>
          </section>
        )
      })}

      <h2 className="section-title">Productos de la investigación</h2>
      <p className="research-note" style={{ color: '#176b45' }}>
        Inventario de productos registrados en la investigación.
      </p>
      <ul className="research-list">
        {productosInvestigacion.map((producto) => (
          // Cada producto usa su id de la API como key única de la lista.
          <li className="research-item" key={producto.id}>
            <strong>{producto.nombre}</strong> — {producto.tipo} — {producto.marca} —
            S/ {Number(producto.precio).toFixed(2)} —{' '}
            {producto.stock === 0 ? 'Agotado' : `Stock: ${producto.stock}`}
            {producto.stock > 0 && producto.stock <= 10 && (
              <strong className="low-stock"> — ¡Últimas unidades!</strong>
            )}
          </li>
        ))}
      </ul>
      {productosInvestigacion.length === 0 && (
        <p className="empty-message">No hay productos registrados.</p>
      )}

      <h2 className="section-title">Clientes y ventas de la investigación</h2>
      <p className="research-note">
        Cada cliente contiene sus ventas; cada venta incluye el producto relacionado y los datos del modelo intermedio.
      </p>
      <ul className="research-list">
        {clientesInvestigacion.map((cliente) => {
          // El total suma el precio unitario por la cantidad de cada venta del cliente.
          const totalVentas = cliente.ventas.reduce(
            (total, venta) => total + Number(venta.precio_unitario) * venta.cantidad,
            0,
          )

          return (
            <li className="research-item" key={cliente.id}>
              <strong>{cliente.nombres} {cliente.apellidos}</strong> — DNI: {cliente.dni}
              <ul className="sale-list">
                {cliente.ventas.map((venta) => (
                  // Venta es el modelo intermedio: relaciona al cliente con el producto.
                  <li className="sale-item" key={venta.id}>
                    {venta.producto.nombre} — {venta.cantidad} unidad(es) x S/ {Number(venta.precio_unitario).toFixed(2)}
                    {' '}— {venta.fecha_venta} — Estado: {venta.estado}
                  </li>
                ))}
              </ul>
              <p className="customer-total">
                {cliente.ventas.length} venta(s) — Total: S/ {totalVentas.toFixed(2)}
              </p>
            </li>
          )
        })}
      </ul>
      {clientesInvestigacion.length === 0 && (
        <p className="empty-message">No hay clientes registrados.</p>
      )}
    </main>
  )
}

export default App
