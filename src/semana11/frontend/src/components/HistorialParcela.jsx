import DiagnosticoForm from './DiagnosticoForm'

function HistorialParcela({ parcela, resumen, onAgregarDiagnostico, children }) {
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

      <section className="resumen-plagas" aria-label="Resumen por plaga">
        <h3>Resumen por diagnóstico</h3>
        <ul>
          {Object.entries(resumen.por_plaga).map(([codigo, cantidad]) => (
            <li key={codigo}>
              <span>{codigo.replace('Potato___', '').replaceAll('_', ' ')}</span>
              <strong>{cantidad}</strong>
            </li>
          ))}
        </ul>
      </section>

      <section className="diagnosticos-seccion">
        <h3>Registros recientes</h3>
        <DiagnosticoForm parcelaId={parcela.id} onAgregar={onAgregarDiagnostico} />
        {children}
      </section>
    </article>
  )
}

export default HistorialParcela
