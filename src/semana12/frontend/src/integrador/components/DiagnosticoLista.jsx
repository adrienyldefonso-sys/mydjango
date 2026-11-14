import DiagnosticoCard from './DiagnosticoCard'

function DiagnosticoLista({
  diagnosticos = [],
  onAgregar,
  onEditar,
  onEliminar,
  eliminandoId,
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
            onEditar={onEditar}
            onEliminar={onEliminar}
            eliminando={eliminandoId === diagnostico.id}
            onCambiarEstado={onCambiarEstado}
          />
        ))}
      </div>
    )
  )
}

export default DiagnosticoLista
