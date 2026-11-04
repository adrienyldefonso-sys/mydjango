import { useState } from 'react'
import DiagnosticoCard from './DiagnosticoCard'

function DiagnosticoLista({ diagnosticos = [] }) {
  const [busqueda, setBusqueda] = useState('')
  // El filtro busca por nombre o código y no distingue mayúsculas.
  const visibles = diagnosticos.filter((diagnostico) => {
    const consulta = busqueda.trim().toLocaleLowerCase('es')
    return [diagnostico.plaga_nombre, diagnostico.plaga_detectada]
      .some((texto) => texto.toLocaleLowerCase('es').includes(consulta))
  })

  return (
    <>
      <label className="buscador-diagnosticos">
        Buscar diagnóstico
        <input
          type="search"
          value={busqueda}
          onChange={(evento) => setBusqueda(evento.target.value)}
          placeholder="Busca por plaga o código"
        />
      </label>

      {visibles.length === 0 ? (
        <p className="estado-vacio">No hay diagnósticos que coincidan con la búsqueda.</p>
      ) : (
        <div className="diagnostico-lista">
          {visibles.map((diagnostico) => (
            <DiagnosticoCard key={diagnostico.id} diagnostico={diagnostico} />
          ))}
        </div>
      )}
    </>
  )
}

export default DiagnosticoLista
