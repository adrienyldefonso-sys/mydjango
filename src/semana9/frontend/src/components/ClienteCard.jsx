import VentaItem from './VentaItem'

function ClienteCard({ cliente }) {
  const totalCliente = cliente.ventas.reduce(
    (total, venta) => total + Number(venta.precio_unitario) * venta.cantidad,
    0,
  )

  return (
    <section className="customer-card">
      <h3 className="customer-name">
        {cliente.nombres} {cliente.apellidos}
      </h3>
      <ul className="sale-list">
        {cliente.ventas.map((venta) => (
          <VentaItem
            key={venta.id}
            producto={venta.producto}
            cantidad={venta.cantidad}
            precioUnitario={venta.precio_unitario}
          />
        ))}
      </ul>
      <p className="customer-total">Total del cliente: S/ {totalCliente.toFixed(2)}</p>
    </section>
  )
}

export default ClienteCard
