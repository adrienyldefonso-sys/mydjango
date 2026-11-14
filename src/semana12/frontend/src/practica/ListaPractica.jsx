import { isAxiosError } from 'axios'
import { useEffect, useState } from 'react'
import api from '../api'

const productoInicial = {
  nombre: '',
  tipo: 'armazon',
  marca: '',
  precio: '',
  stock: '0',
}

function ListaPractica() {
  const [productos, setProductos] = useState([])
  const [buscar, setBuscar] = useState('')
  const [cargando, setCargando] = useState(true)
  const [errorCarga, setErrorCarga] = useState('')
  const [formulario, setFormulario] = useState(productoInicial)
  const [errorCreacion, setErrorCreacion] = useState(null)
  const [mensajeExito, setMensajeExito] = useState('')
  const [guardando, setGuardando] = useState(false)
  const [operando, setOperando] = useState(false)
  const [errorOperacion, setErrorOperacion] = useState(null)
  const [mensajeOperacion, setMensajeOperacion] = useState('')

  const actualizarBusqueda = (event) => {
    setBuscar(event.target.value)
    setCargando(true)
    setErrorCarga('')
  }

  useEffect(() => {
    let efectoActivo = true

    const cargarProductos = async () => {
      try {
        const respuesta = await api.get('/productos/', {
          params: { search: buscar },
        })
        if (efectoActivo) {
          setProductos(respuesta.data)
        }
      } catch (errorPeticion) {
        if (efectoActivo) {
          console.error('No se pudo cargar la lista.', errorPeticion)
          setErrorCarga('No se pudo cargar la lista.')
        }
      } finally {
        if (efectoActivo) {
          setCargando(false)
        }
      }
    }

    cargarProductos()
    return () => {
      efectoActivo = false
    }
  }, [buscar])

  const actualizarCampo = (event) => {
    const { name, value } = event.target
    setFormulario((actual) => ({ ...actual, [name]: value }))
  }

  const crearProducto = async (event) => {
    event.preventDefault()
    setGuardando(true)
    setErrorCreacion(null)
    setMensajeExito('')

    try {
      const respuesta = await api.post('/productos/', {
        ...formulario,
        precio: Number(formulario.precio),
        stock: Number(formulario.stock),
      })
      setProductos((actuales) => [...actuales, respuesta.data])
      setFormulario(productoInicial)
      setMensajeExito(`Producto creado correctamente (HTTP ${respuesta.status}).`)
    } catch (errorPeticion) {
      if (isAxiosError(errorPeticion) && errorPeticion.response) {
        setErrorCreacion(errorPeticion.response.data)
      } else {
        console.error('No se pudo crear el producto:', errorPeticion)
        setErrorCreacion({ detail: 'No se pudo conectar con el servidor.' })
      }
    } finally {
      setGuardando(false)
    }
  }

  const actualizarStock = async (producto) => {
    setOperando(true)
    setErrorOperacion(null)
    setMensajeOperacion('')

    try {
      const respuesta = await api.patch(`/productos/${producto.id}/`, {
        stock: producto.stock + 1,
      })
      setProductos((actuales) =>
        actuales.map((actual) =>
          actual.id === producto.id ? respuesta.data : actual,
        ),
      )
      setMensajeOperacion(`Stock actualizado (HTTP ${respuesta.status}).`)
    } catch (errorPeticion) {
      if (isAxiosError(errorPeticion) && errorPeticion.response) {
        setErrorOperacion(errorPeticion.response.data)
      } else {
        console.error('No se pudo actualizar el producto:', errorPeticion)
        setErrorOperacion({ detail: 'No se pudo actualizar el producto.' })
      }
    } finally {
      setOperando(false)
    }
  }

  const eliminarProducto = async (id) => {
    setOperando(true)
    setErrorOperacion(null)
    setMensajeOperacion('')

    try {
      const respuesta = await api.delete(`/productos/${id}/`)
      if (respuesta.status !== 204) {
        throw new Error(`Se esperaba HTTP 204; se recibió ${respuesta.status}.`)
      }
      setProductos((actuales) => actuales.filter((producto) => producto.id !== id))
      setMensajeOperacion(`Producto eliminado (HTTP ${respuesta.status}).`)
    } catch (errorPeticion) {
      if (isAxiosError(errorPeticion) && errorPeticion.response) {
        setErrorOperacion(errorPeticion.response.data)
      } else {
        console.error('No se pudo eliminar el producto:', errorPeticion)
        setErrorOperacion({
          detail: errorPeticion instanceof Error
            ? errorPeticion.message
            : 'No se pudo eliminar el producto.',
        })
      }
    } finally {
      setOperando(false)
    }
  }

  return (
    <section aria-labelledby="productos-titulo">
      <h2 id="productos-titulo">Productos</h2>
      <label className="busqueda-productos">
        Buscar productos
        <input
          type="search"
          value={buscar}
          onChange={actualizarBusqueda}
          placeholder="Nombre, marca o tipo"
        />
      </label>
      <form className="producto-formulario" onSubmit={crearProducto}>
        <h3>Crear producto</h3>
        <label>
          Nombre
          <input
            name="nombre"
            value={formulario.nombre}
            onChange={actualizarCampo}
            required
          />
        </label>
        <label>
          Tipo
          <select name="tipo" value={formulario.tipo} onChange={actualizarCampo}>
            <option value="armazon">Armazón</option>
            <option value="luna">Luna</option>
            <option value="lente_contacto">Lente de contacto</option>
          </select>
        </label>
        <label>
          Marca
          <input
            name="marca"
            value={formulario.marca}
            onChange={actualizarCampo}
          />
        </label>
        <label>
          Precio
          <input
            name="precio"
            type="number"
            step="0.01"
            value={formulario.precio}
            onChange={actualizarCampo}
            required
          />
        </label>
        <small>El precio debe ser mayor que cero. Usa 0 para probar la validación del servidor.</small>
        <label>
          Stock
          <input
            name="stock"
            type="number"
            min="0"
            step="1"
            value={formulario.stock}
            onChange={actualizarCampo}
            required
          />
        </label>
        <button type="submit" disabled={guardando}>
          {guardando ? 'Guardando...' : 'Crear producto'}
        </button>
        {mensajeExito && <p role="status">{mensajeExito}</p>}
        {errorCreacion && (
          <div role="alert">
            <p>El servidor rechazó el registro:</p>
            <pre>{JSON.stringify(errorCreacion, null, 2)}</pre>
          </div>
        )}
      </form>

      {mensajeOperacion && <p role="status">{mensajeOperacion}</p>}
      {errorOperacion && (
        <div role="alert">
          <p>No se pudo completar la operación:</p>
          <pre>{JSON.stringify(errorOperacion, null, 2)}</pre>
        </div>
      )}

      {cargando ? (
        <p role="status">Cargando...</p>
      ) : errorCarga ? (
        <p role="alert">{errorCarga}</p>
      ) : productos.length === 0 ? (
        <p>No hay productos registrados.</p>
      ) : (
        <ul className="productos-lista">
          {productos.map((producto) => (
            <li className="producto" key={producto.id}>
              <strong>{producto.nombre}</strong>
              <span>{producto.marca} · {producto.tipo}</span>
              <span>Precio: S/ {producto.precio} · Stock: {producto.stock}</span>
              <div className="producto-acciones">
                <button
                  type="button"
                  disabled={operando}
                  onClick={() => actualizarStock(producto)}
                >
                  Aumentar stock (+1)
                </button>
                <button
                  type="button"
                  disabled={operando}
                  onClick={() => eliminarProducto(producto.id)}
                >
                  Eliminar
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}

export default ListaPractica
