function VentaItem({ producto, cantidad, precioUnitario }) {
  return (
    <li className="sale-item">
      {producto} — {cantidad} unidad(es) x S/ {Number(precioUnitario).toFixed(2)}
    </li>
  )
}

export default VentaItem
