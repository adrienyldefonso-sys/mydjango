import { useState } from 'react'

function ProductoItem({
  nombre,
  precio,
  stock,
  // Si el padre no envía marca, se muestra este texto.
  marca = 'Marca no especificada',
}) {
  const [revisiones, setRevisiones] = useState(0)

  return (
    <li className="product-item">
      <div>
        {nombre} ({marca}) — S/ {Number(precio).toFixed(2)} —{' '}
        {stock === 0 ? 'Agotado' : `Stock: ${stock}`}
        {stock > 0 && stock <= 10 && (
          <strong className="low-stock"> — ¡Últimas unidades!</strong>
        )}
      </div>
      <button
        type="button"
        disabled={stock === 0}
        onClick={() => setRevisiones((actuales) => actuales + 1)}
      >
        Registrar revisión
      </button>
      {revisiones > 0 && (
        <p className="revision-count">
          Revisado {revisiones} {revisiones === 1 ? 'vez' : 'veces'}
        </p>
      )}
    </li>
  )
}

export default ProductoItem
