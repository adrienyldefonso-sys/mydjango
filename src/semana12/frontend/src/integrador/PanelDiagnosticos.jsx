import { isAxiosError, isCancel } from 'axios'
import { useCallback, useEffect, useState } from 'react'
import { apiOjoChakra as api } from '../api'
import Aviso from './components/Aviso'
import Buscador from './components/Buscador'
import Carrito from './components/Carrito'
import DiagnosticoLista from './components/DiagnosticoLista'
import HistorialParcela from './components/HistorialParcela'
import ResumenDiagnosticos from './components/ResumenDiagnosticos'

function adaptarParcela(parcela) {
  return {
    ...parcela,
    latitud: Number(parcela.latitud),
    longitud: Number(parcela.longitud),
  }
}

function adaptarDiagnostico(diagnostico, activo = true) {
  return {
    ...diagnostico,
    confianza: Number(diagnostico.confianza),
    activo,
  }
}

function PanelDiagnosticos() {
  const [parcela, setParcela] = useState(null)
  const [diagnosticos, setDiagnosticos] = useState([])
  const [parcelasCargadas, setParcelasCargadas] = useState(false)
  const [cargando, setCargando] = useState(true)
  const [errorCarga, setErrorCarga] = useState('')
  const [diagnosticoSeleccionado, setDiagnosticoSeleccionado] = useState(null)
  const [errorFormulario, setErrorFormulario] = useState(null)
  const [mensajeFormulario, setMensajeFormulario] = useState('')
  const [guardando, setGuardando] = useState(false)
  const [carrito, setCarrito] = useState([])
  const [busqueda, setBusqueda] = useState('')
  const [filtroPlaga, setFiltroPlaga] = useState('')
  const [aviso, setAviso] = useState(null)
  const [mensajeEliminacion, setMensajeEliminacion] = useState(null)
  const [eliminandoId, setEliminandoId] = useState(null)
  const ocultarAviso = useCallback(() => setAviso(null), [])

  useEffect(() => {
    let efectoActivo = true
    const controlador = new AbortController()

    async function cargarParcela() {
      try {
        const respuestaParcelas = await api.get('/parcelas/', {
          signal: controlador.signal,
        })
        const primeraParcela = respuestaParcelas.data[0]

        if (efectoActivo) {
          setParcela(primeraParcela ? adaptarParcela(primeraParcela) : null)
        }
      } catch (errorPeticion) {
        if (isCancel(errorPeticion)) {
          return
        }
        if (efectoActivo) {
          console.error('No se pudieron cargar las parcelas.', errorPeticion)
          setErrorCarga('No se pudo cargar la parcela.')
        }
      } finally {
        if (efectoActivo) {
          setParcelasCargadas(true)
        }
      }
    }

    cargarParcela()
    return () => {
      efectoActivo = false
      controlador.abort()
    }
  }, [])

  useEffect(() => {
    if (!parcelasCargadas || !parcela) {
      return undefined
    }

    let efectoActivo = true
    const controlador = new AbortController()

    async function cargarDiagnosticos() {
      setCargando(true)
      setErrorCarga('')
      try {
        const respuesta = await api.get('/diagnosticos/', {
          params: {
            parcela: parcela.id,
            ...(busqueda.trim() ? { search: busqueda.trim() } : {}),
            ...(filtroPlaga ? { plaga_detectada: filtroPlaga } : {}),
          },
          signal: controlador.signal,
        })
        if (efectoActivo) {
          setDiagnosticos(respuesta.data.map((diagnostico) => (
            adaptarDiagnostico(diagnostico)
          )))
        }
      } catch (errorPeticion) {
        if (isCancel(errorPeticion)) {
          return
        }
        if (efectoActivo) {
          console.error('No se pudo cargar el historial de diagnósticos.', errorPeticion)
          setErrorCarga('No se pudo cargar el historial de diagnósticos.')
          setDiagnosticos([])
        }
      } finally {
        if (efectoActivo) {
          setCargando(false)
        }
      }
    }

    cargarDiagnosticos()
    return () => {
      efectoActivo = false
      controlador.abort()
    }
  }, [busqueda, filtroPlaga, parcela, parcelasCargadas])

  function cumpleFiltros(diagnostico) {
    const terminos = busqueda.trim().toLocaleLowerCase('es').split(/\s+/).filter(Boolean)
    const camposBuscables = [
      diagnostico.plaga_nombre,
      diagnostico.plaga_detectada,
    ].map((texto) => texto.toLocaleLowerCase('es'))

    return (
      (!filtroPlaga || diagnostico.plaga_detectada === filtroPlaga)
      && terminos.every((termino) => (
        camposBuscables.some((texto) => texto.includes(termino))
      ))
    )
  }

  const resumen = diagnosticos.reduce((actual, diagnostico) => {
    const ultimaFecha = actual.ultima_fecha
    const fechaDiagnostico = diagnostico.fecha_captura

    return {
      total: actual.total + 1,
      ultima_fecha: !ultimaFecha || new Date(fechaDiagnostico) > new Date(ultimaFecha)
        ? fechaDiagnostico
        : ultimaFecha,
      por_plaga: {
        ...actual.por_plaga,
        [diagnostico.plaga_detectada]:
          (actual.por_plaga[diagnostico.plaga_detectada] ?? 0) + 1,
      },
    }
  }, { total: 0, ultima_fecha: null, por_plaga: {} })

  async function guardarDiagnostico(datos) {
    setGuardando(true)
    setErrorFormulario(null)
    setMensajeFormulario('')

    try {
      if (diagnosticoSeleccionado) {
        const respuesta = await api.patch(
          `/diagnosticos/${diagnosticoSeleccionado.id}/`,
          datos,
        )
        const actualizado = adaptarDiagnostico(
          respuesta.data,
          diagnosticoSeleccionado.activo,
        )
        setDiagnosticos((actuales) => (
          cumpleFiltros(actualizado)
            ? actuales.map((diagnostico) => (
              diagnostico.id === actualizado.id ? actualizado : diagnostico
            ))
            : actuales.filter((diagnostico) => diagnostico.id !== actualizado.id)
        ))
        setMensajeFormulario(`Diagnóstico actualizado (HTTP ${respuesta.status}).`)
        setDiagnosticoSeleccionado(null)
      } else {
        const respuesta = await api.post('/diagnosticos/', datos)
        const creado = adaptarDiagnostico(respuesta.data)
        if (cumpleFiltros(creado)) {
          setDiagnosticos((actuales) => [creado, ...actuales])
        }
        setMensajeFormulario(`Diagnóstico creado (HTTP ${respuesta.status}).`)
      }
      return true
    } catch (errorPeticion) {
      if (isAxiosError(errorPeticion) && errorPeticion.response) {
        setErrorFormulario(errorPeticion.response.data)
      } else {
        console.error('No se pudo guardar el diagnóstico:', errorPeticion)
        setErrorFormulario({ detail: 'No se pudo conectar con el servidor.' })
      }
      return false
    } finally {
      setGuardando(false)
    }
  }

  function seleccionarParaEditar(diagnostico) {
    setDiagnosticoSeleccionado(diagnostico)
    setErrorFormulario(null)
    setMensajeFormulario('')
  }

  function cancelarEdicion() {
    setDiagnosticoSeleccionado(null)
    setErrorFormulario(null)
    setMensajeFormulario('')
  }

  async function eliminarDiagnostico(diagnostico) {
    const confirmado = window.confirm(
      `¿Deseas eliminar el diagnóstico "${diagnostico.plaga_nombre}"?`,
    )
    if (!confirmado) {
      return
    }

    setEliminandoId(diagnostico.id)
    setMensajeEliminacion(null)
    try {
      const respuesta = await api.delete(`/diagnosticos/${diagnostico.id}/`)
      if (respuesta.status !== 204) {
        setMensajeEliminacion({
          tipo: 'error',
          texto: `La API respondió HTTP ${respuesta.status}; se esperaba 204.`,
        })
        return
      }

      setDiagnosticos((actuales) => (
        actuales.filter((actual) => actual.id !== diagnostico.id)
      ))
      setCarrito((actuales) => (
        actuales.filter((linea) => linea.id !== diagnostico.id)
      ))
      setDiagnosticoSeleccionado((actual) => (
        actual?.id === diagnostico.id ? null : actual
      ))
      setMensajeEliminacion({
        tipo: 'success',
        texto: `Diagnóstico eliminado (HTTP ${respuesta.status}).`,
      })
    } catch (errorPeticion) {
      if (isAxiosError(errorPeticion) && errorPeticion.response?.status === 404) {
        setMensajeEliminacion({
          tipo: 'error',
          texto: 'El diagnóstico ya no existe en el servidor (HTTP 404). Actualiza la página para sincronizar la lista.',
        })
      } else if (isAxiosError(errorPeticion) && errorPeticion.response) {
        console.error('No se pudo eliminar el diagnóstico:', errorPeticion)
        setMensajeEliminacion({
          tipo: 'error',
          texto: `No se pudo eliminar el diagnóstico (HTTP ${errorPeticion.response.status}).`,
        })
      } else {
        console.error('No se pudo eliminar el diagnóstico:', errorPeticion)
        setMensajeEliminacion({
          tipo: 'error',
          texto: 'No se pudo conectar con el servidor.',
        })
      }
    } finally {
      setEliminandoId(null)
    }
  }

  function cambiarEstadoDiagnostico(id) {
    setDiagnosticos((actuales) => actuales.map((diagnostico) => (
      diagnostico.id === id
        ? { ...diagnostico, activo: !diagnostico.activo }
        : diagnostico
    )))
  }

  function agregarAlCarrito(diagnostico) {
    setAviso({ nombre: diagnostico.plaga_nombre })
    setCarrito((actuales) => {
      const yaAgregado = actuales.some((linea) => linea.id === diagnostico.id)

      if (yaAgregado) {
        return actuales.map((linea) => (
          linea.id === diagnostico.id
            ? { ...linea, cantidad: linea.cantidad + 1 }
            : linea
        ))
      }

      return [
        ...actuales,
        {
          id: diagnostico.id,
          nombre: diagnostico.plaga_nombre,
          confianza: diagnostico.confianza,
          cantidad: 1,
        },
      ]
    })
  }

  function quitarDelCarrito(id) {
    setCarrito((actuales) => actuales.filter((linea) => linea.id !== id))
  }

  function vaciarCarrito() {
    setCarrito([])
  }

  return (
    <main className="pagina integrador">
      <header className="hero">
        <div className="marca">Ojo d’Chakra</div>
        <p className="eyebrow">Monitoreo agrónomo · Cultivo de papa</p>
        <h1>Panel de diagnósticos</h1>
        <p>Revisa y administra los diagnósticos de tu parcela.</p>
      </header>

      {!parcelasCargadas ? (
        <p role="status">Cargando diagnósticos...</p>
      ) : errorCarga && !parcela ? (
        <p role="alert">{errorCarga}</p>
      ) : !parcela ? (
        <p className="estado-vacio">La API no tiene parcelas registradas.</p>
      ) : (
        <>
          <Buscador
            valor={busqueda}
            onCambiar={setBusqueda}
            filtroPlaga={filtroPlaga}
            onCambiarFiltro={setFiltroPlaga}
          />
          {cargando && <p role="status">Actualizando resultados...</p>}
          {errorCarga && <p role="alert">{errorCarga}</p>}
          <Aviso aviso={aviso} onCerrar={ocultarAviso} />
          {mensajeEliminacion && (
            <p
              className={`form-feedback ${mensajeEliminacion.tipo}`}
              role={mensajeEliminacion.tipo === 'error' ? 'alert' : 'status'}
            >
              {mensajeEliminacion.texto}
            </p>
          )}
          <section className="historial-lista" aria-label="Parcelas con historial">
            <HistorialParcela
              parcela={parcela}
              resumen={resumen}
              diagnosticoSeleccionado={diagnosticoSeleccionado}
              errorFormulario={errorFormulario}
              mensajeFormulario={mensajeFormulario}
              guardando={guardando}
              onGuardarDiagnostico={guardarDiagnostico}
              onCancelarEdicion={cancelarEdicion}
            >
              <div className="resumen-y-lista">
                <ResumenDiagnosticos
                  total={resumen.total}
                  porPlaga={resumen.por_plaga}
                />
                <DiagnosticoLista
                  diagnosticos={diagnosticos}
                  onAgregar={agregarAlCarrito}
                  onEditar={seleccionarParaEditar}
                  onEliminar={eliminarDiagnostico}
                  eliminandoId={eliminandoId}
                  onCambiarEstado={cambiarEstadoDiagnostico}
                />
              </div>
            </HistorialParcela>
          </section>
          <Carrito
            lineas={carrito}
            onQuitar={quitarDelCarrito}
            onVaciar={vaciarCarrito}
          />
        </>
      )}
    </main>
  )
}

export default PanelDiagnosticos
