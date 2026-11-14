import { useState } from 'react'
import ListaPractica from './practica/ListaPractica'
import PanelDiagnosticos from './integrador/PanelDiagnosticos'

function App() {
  const [vista, setVista] = useState('practica')

  return (
    <>
      <nav className="secciones-laboratorio" aria-label="Secciones del laboratorio">
        <button
          type="button"
          aria-pressed={vista === 'practica'}
          onClick={() => setVista('practica')}
        >
          Parte 1: práctica
        </button>
        <button
          type="button"
          aria-pressed={vista === 'integrador'}
          onClick={() => setVista('integrador')}
        >
          Parte 2: Ojo d’Chakra
        </button>
      </nav>
      {vista === 'integrador' ? (
        <PanelDiagnosticos />
      ) : (
        <main>
          <h1>Semana 12 — AJAX con React</h1>
          <p>Consulta y crea productos mediante la API REST de Django.</p>
          <ListaPractica />
        </main>
      )}
    </>
  )
}

export default App
