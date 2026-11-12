import { useCallback, useState } from 'react'
import Aviso from './Aviso'
import Buscador from './Buscador'
import Carrito from './Carrito'
import DiagnosticoLista from './DiagnosticoLista'
import HistorialParcela from './HistorialParcela'
import ResumenDiagnosticos from './ResumenDiagnosticos'
import { mockHistorialData } from '../data/mockHistorial'

function PanelDiagnosticos() {
  // El panel es dueño del arreglo compartido entre el formulario, el filtro y el resumen.
  const [diagnosticos, setDiagnosticos] = useState(() => (
    mockHistorialData.diagnosticos.map((diagnostico) => ({
      ...diagnostico,
      activo: true,
    }))
  ))
  const [carrito, setCarrito] = useState([])
  const [busqueda, setBusqueda] = useState('')
  const [aviso, setAviso] = useState(null)
  const consulta = busqueda.trim().toLocaleLowerCase('es')
  const ocultarAviso = useCallback(() => setAviso(null), [])
  const parcela = mockHistorialData.parcela

  // El resumen sale del estado con reduce; no se guarda una copia en useState.
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

  // Recibe el registro válido del formulario y agrega un arreglo nuevo al estado.
  function guardarDiagnostico(diagnostico) {
    setDiagnosticos((actuales) => [
      { ...diagnostico, activo: true },
      ...actuales,
    ])
  }

  function eliminarDiagnostico(id) {
    // filter crea una lista nueva sin el registro; el padre también limpia su línea del carrito.
    setDiagnosticos((actuales) => (
      actuales.filter((diagnostico) => diagnostico.id !== id)
    ))
    setCarrito((actuales) => actuales.filter((linea) => linea.id !== id))
  }

  function cambiarEstadoDiagnostico(id) {
    // map conserva los demás registros y crea una copia con el estado invertido para el id elegido.
    setDiagnosticos((actuales) => (
      actuales.map((diagnostico) => (
        diagnostico.id === id
          ? { ...diagnostico, activo: !diagnostico.activo }
          : diagnostico
      ))
    ))
  }

  function agregarAlCarrito(diagnostico) {
    // Un objeto nuevo reinicia el temporizador aunque se agregue el mismo diagnóstico.
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

  // El valor controlado de Buscador filtra la misma lista que alimenta el resumen.
  const diagnosticosFiltrados = diagnosticos.filter((diagnostico) => (
    [diagnostico.plaga_nombre, diagnostico.plaga_detectada]
      .some((texto) => texto.toLocaleLowerCase('es').includes(consulta))
  ))

  return (
    <main className="pagina">
      <header className="hero">
        <div className="marca">Ojo d’Chakra</div>
        <p className="eyebrow">Monitoreo agrónomo · Cultivo de papa</p>
        <h1>Panel de diagnósticos</h1>
        <p>Revisa y administra los diagnósticos de tu parcela.</p>
      </header>

      <Buscador valor={busqueda} onCambiar={setBusqueda} />
      <Aviso aviso={aviso} onCerrar={ocultarAviso} />
      <section className="historial-lista" aria-label="Parcelas con historial">
        <HistorialParcela
          parcela={parcela}
          resumen={resumen}
          onGuardarDiagnostico={guardarDiagnostico}
        >
          <div className="resumen-y-lista">
            {/* Resumen y listado son hermanos y reciben datos derivados del mismo estado. */}
            <ResumenDiagnosticos
              total={resumen.total}
              porPlaga={resumen.por_plaga}
            />
            <DiagnosticoLista
              diagnosticos={diagnosticosFiltrados}
              onAgregar={agregarAlCarrito}
              onEliminar={eliminarDiagnostico}
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
    </main>
  )
}

export default PanelDiagnosticos
