import DiagnosticoCard from './DiagnosticoCard'

function DiagnosticoLista({
  diagnosticos = [],
  onAgregar,
  onEliminar,
  onCambiarEstado,
}) {
  // La lista pasa los callbacks del padre a cada fila; cada fila solo comunica la acción.
  return (
    diagnosticos.length === 0 ? (
      <p className="estado-vacio">No hay diagnósticos que coincidan.</p>
    ) : (
      <div className="diagnostico-lista">
        {diagnosticos.map((diagnostico) => (
          <DiagnosticoCard
            key={diagnostico.id}
            diagnostico={diagnostico}
            onAgregar={onAgregar}
            onEliminar={onEliminar}
            onCambiarEstado={onCambiarEstado}
          />
        ))}
      </div>
    )
  )
}

export default DiagnosticoLista
