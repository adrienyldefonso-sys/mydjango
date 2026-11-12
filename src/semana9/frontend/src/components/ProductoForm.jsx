import { useState } from 'react'

function ProductoForm({ onAgregarProducto }) {
  const [nombre, setNombre] = useState('')
  const [tipo, setTipo] = useState('armazon')
  const [marca, setMarca] = useState('')
  const [precio, setPrecio] = useState('')
  const [stock, setStock] = useState('0')
  const [error, setError] = useState('')
  const [guardando, setGuardando] = useState(false)

  async function enviar(evento) {
    evento.preventDefault()

    // Regla de ProductoSerializer de Semana 8: el precio debe ser mayor que cero.
    if (!Number.isFinite(Number(precio)) || Number(precio) <= 0) {
      setError('El precio debe ser mayor que cero.')
      return
    }

    if (!nombre.trim()) {
      setError('El nombre es obligatorio.')
      return
    }

    if (!Number.isInteger(Number(stock)) || Number(stock) < 0) {
      setError('El stock debe ser un entero mayor o igual a cero.')
      return
    }

    setGuardando(true)
    setError('')

    try {
      await onAgregarProducto({
        nombre: nombre.trim(),
        tipo,
        marca: marca.trim(),
        precio: Number(precio).toFixed(2),
        stock: Number(stock),
      })
      setNombre('')
      setTipo('armazon')
      setMarca('')
      setPrecio('')
      setStock('0')
    } catch (error) {
      setError(error.message)
    } finally {
      setGuardando(false)
    }
  }

  return (
    <form className="producto-form" onSubmit={enviar}>
      <h3>Registrar producto</h3>
      <div className="producto-form-grid">
        <label>
          Nombre
          <input value={nombre} onChange={(e) => setNombre(e.target.value)} />
        </label>
        <label>
          Tipo
          <select value={tipo} onChange={(e) => setTipo(e.target.value)}>
            <option value="armazon">Armazón</option>
            <option value="luna">Luna</option>
            <option value="lente_contacto">Lente de contacto</option>
          </select>
        </label>
        <label>
          Marca
          <input value={marca} onChange={(e) => setMarca(e.target.value)} />
        </label>
        <label>
          Precio
          <input type="number" step="0.01" value={precio} onChange={(e) => setPrecio(e.target.value)} />
        </label>
        <label>
          Stock
          <input type="number" min="0" step="1" value={stock} onChange={(e) => setStock(e.target.value)} />
        </label>
      </div>
      <button type="submit" disabled={guardando}>
        {guardando ? 'Guardando…' : 'Agregar producto'}
      </button>
      {error && <p className="error-text" role="alert">{error}</p>}
    </form>
  )
}

export default ProductoForm
