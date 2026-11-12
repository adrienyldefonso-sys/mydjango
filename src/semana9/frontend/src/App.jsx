import { useEffect, useState } from 'react'
import { clientesConVentas } from './datos'
import ProductoLista from './components/ProductoLista'
import ClienteCard from './components/ClienteCard'
import Tarjeta from './components/Tarjeta'

function App() {
  const [productos, setProductos] = useState([])
  const [cargandoProductos, setCargandoProductos] = useState(true)
  const [errorProductos, setErrorProductos] = useState('')

  useEffect(() => {
    const controller = new AbortController()

    async function cargarProductos() {
      try {
        const respuesta = await fetch('/django-api/optica-v3/api/productos/', {
          signal: controller.signal,
        })

        if (!respuesta.ok) {
          throw new Error(`No se pudieron cargar los productos (HTTP ${respuesta.status}).`)
        }

        setProductos(await respuesta.json())
      } catch (error) {
        if (error.name !== 'AbortError') {
          setErrorProductos(error.message)
        }
      } finally {
        if (!controller.signal.aborted) {
          setCargandoProductos(false)
        }
      }
    }

    cargarProductos()
    return () => controller.abort()
  }, [])

  async function agregarProducto(datos) {
    const respuesta = await fetch('/django-api/optica-v3/api/productos/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(datos),
    })
    const resultado = await respuesta.json()

    if (!respuesta.ok) {
      throw new Error(
        typeof resultado === 'object' ? JSON.stringify(resultado) : 'No se pudo guardar el producto.',
      )
    }

    setProductos((actuales) => [...actuales, resultado])
  }

  return (
    <main className="page">
      <h1 className="page-title">Sistema de Óptica</h1>

      <Tarjeta titulo="Productos">
        {cargandoProductos && <p role="status">Cargando productos…</p>}
        {errorProductos && <p className="error-text" role="alert">{errorProductos}</p>}
        {!cargandoProductos && !errorProductos && (
          <ProductoLista productos={productos} onAgregarProducto={agregarProducto} />
        )}
      </Tarjeta>

      <h2 className="section-title">Ventas por cliente</h2>
      {clientesConVentas.map((cliente) => (
        <ClienteCard key={cliente.id} cliente={cliente} />
      ))}
    </main>
  )
}

export default App
