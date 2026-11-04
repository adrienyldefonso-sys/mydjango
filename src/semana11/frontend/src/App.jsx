import { useState } from 'react'
import DiagnosticoLista from './components/DiagnosticoLista'
import HistorialParcela from './components/HistorialParcela'
import { parcelasMock } from './data/mockHistorial'

function App() {
  const [parcelas, setParcelas] = useState(parcelasMock)

  function agregarDiagnostico(parcelaId, diagnostico) {
    setParcelas((actuales) => actuales.map((registro) => {
      if (registro.parcela.id !== parcelaId) {
        return registro
      }

      const porPlaga = {
        ...registro.resumen.por_plaga,
        [diagnostico.plaga_detectada]:
          (registro.resumen.por_plaga[diagnostico.plaga_detectada] ?? 0) + 1,
      }
      const ultimaActual = registro.resumen.ultima_fecha
      const ultimaNueva = diagnostico.fecha_captura

      return {
        ...registro,
        diagnosticos: [diagnostico, ...registro.diagnosticos],
        resumen: {
          total: registro.resumen.total + 1,
          ultima_fecha: !ultimaActual || new Date(ultimaNueva) > new Date(ultimaActual)
            ? ultimaNueva
            : ultimaActual,
          por_plaga: porPlaga,
        },
      }
    }))
  }

  return (
    <main className="pagina">
      <header className="hero">
        <div className="marca">Ojo d’Chakra</div>
        <p className="eyebrow">Monitoreo agrónomo · Cultivo de papa</p>
        <h1>Historial de diagnósticos</h1>
        <p>Revisa la evolución de salud y plagas detectadas en tus parcelas.</p>
      </header>

      <section className="historial-lista" aria-label="Parcelas con historial">
        {parcelas.map(({ parcela, resumen, diagnosticos }) => (
          <HistorialParcela
            key={parcela.id}
            parcela={parcela}
            resumen={resumen}
            onAgregarDiagnostico={(diagnostico) => agregarDiagnostico(parcela.id, diagnostico)}
          >
            <DiagnosticoLista diagnosticos={diagnosticos} />
          </HistorialParcela>
        ))}
      </section>
    </main>
  )
}

export default App
