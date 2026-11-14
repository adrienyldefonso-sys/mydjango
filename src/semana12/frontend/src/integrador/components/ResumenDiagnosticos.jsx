function ResumenDiagnosticos({ total, porPlaga }) {
  // El padre deriva estos valores con reduce y los pasa por props; aquí no hay estado duplicado.
  return (
    <section className="resumen-plagas" aria-label="Resumen por plaga">
      <h3>Resumen de diagnósticos</h3>
      <p className="resumen-total"><strong>Total:</strong> {total}</p>
      <ul>
        {Object.entries(porPlaga).map(([codigo, cantidad]) => (
          <li key={codigo}>
            <span>{codigo.replace('Potato___', '').replaceAll('_', ' ')}</span>
            <strong>{cantidad}</strong>
          </li>
        ))}
      </ul>
    </section>
  )
}

export default ResumenDiagnosticos
