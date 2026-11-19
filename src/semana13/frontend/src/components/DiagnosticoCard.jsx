function DiagnosticoCard({ diagnostico }) {
  const fecha = new Intl.DateTimeFormat('es-PE', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(diagnostico.fecha_captura))

  return (
    <article>
      <h2>{diagnostico.plaga_nombre}</h2>
      <p>Código: {diagnostico.plaga_detectada}</p>
      <p>Confianza: {Number(diagnostico.confianza).toFixed(2)}%</p>
      <time dateTime={diagnostico.fecha_captura}>{fecha}</time>
    </article>
  )
}

export default DiagnosticoCard