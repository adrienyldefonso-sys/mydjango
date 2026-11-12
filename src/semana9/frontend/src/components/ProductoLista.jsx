import { useState } from 'react'
import ProductoItem from './ProductoItem'
import ProductoForm from './ProductoForm'

function ProductoLista({ productos, onAgregarProducto }) {
  const [busqueda, setBusqueda] = useState('')
  // La búsqueda ignora mayúsculas; el estado controla el valor del input.
  const visibles = productos.filter((producto) =>
    producto.nombre.toLowerCase().includes(busqueda.toLowerCase()),
  )

  return (
    <>
      <ProductoForm onAgregarProducto={onAgregarProducto} />

      <label className="buscador-productos">
        Buscar producto
        <input
          type="search"
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
          placeholder="Escribe un nombre"
        />
      </label>

      {visibles.length === 0 ? (
        <p className="empty-message">No hay productos que coincidan con la búsqueda.</p>
      ) : (
        <ul className="product-list">
          {/* map crea una fila por producto y su id es la key estable. */}
          {visibles.map((producto) => (
            <ProductoItem
              key={producto.id}
              nombre={producto.nombre}
              precio={producto.precio}
              stock={producto.stock}
              marca={producto.marca}
            />
          ))}
        </ul>
      )}
    </>
  )
}

export default ProductoLista
