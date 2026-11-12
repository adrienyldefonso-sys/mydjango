import DiagnosticoForm from './DiagnosticoForm'

function HistorialParcela({ parcela, resumen, onGuardarDiagnostico, children }) {
  const ultimaFecha = resumen.ultima_fecha
    ? new Intl.DateTimeFormat('es-PE', { dateStyle: 'long' }).format(
      new Date(resumen.ultima_fecha),
    )
    : 'Sin diagnósticos'

  return (
    <article className="parcela-card">
      <header className="parcela-header">
        <div>
          <p className="eyebrow">Historial de parcela</p>
          <h2>{parcela.nombre}</h2>
          <p>{parcela.cultivo} · {parcela.referencia}</p>
        </div>
        <span className="total-badge">{resumen.total} diagnósticos</span>
      </header>

      <div className="parcela-meta">
        <span><strong>Agricultor:</strong> {parcela.agricultor}</span>
        <span><strong>Coordenadas:</strong> {parcela.latitud}, {parcela.longitud}</span>
        <span><strong>Último registro:</strong> {ultimaFecha}</span>
      </div>

      <section className="diagnosticos-seccion">
        <h3>Registros recientes</h3>
        {/* El formulario controlado envía el registro válido al padre mediante onGuardar. */}
        <DiagnosticoForm parcelaId={parcela.id} onGuardar={onGuardarDiagnostico} />
        {children}
      </section>
    </article>
  )
}

export default HistorialParcela
