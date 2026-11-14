import { useEffect } from 'react'

function Carrito({ lineas = [], onQuitar, onVaciar }) {
  const { unidades, confianzaAcumulada } = lineas.reduce(
    (totales, linea) => ({
      unidades: totales.unidades + linea.cantidad,
      confianzaAcumulada:
        totales.confianzaAcumulada + Number(linea.confianza) * linea.cantidad,
    }),
    { unidades: 0, confianzaAcumulada: 0 },
  )

  // [unidades] vuelve a ejecutar el efecto cuando cambia el carrito y su limpieza restaura el título.
  useEffect(() => {
    const tituloAnterior = document.title
    document.title = `Carrito (${unidades}) — Diagnósticos`
    console.log(`Carrito actualizado: ${unidades} unidades`)

    return () => {
      document.title = tituloAnterior
    }
  }, [unidades])

  return (
    <section className="carrito" aria-label="Diagnósticos seleccionados">
      <h2>Diagnósticos seleccionados</h2>
      <div className="carrito-totales">
        <p><strong>Unidades:</strong> {unidades}</p>
        <p>
          <strong>Suma de confianza:</strong>{' '}
          {confianzaAcumulada.toFixed(2)} puntos
        </p>
      </div>
      <p className="carrito-nota">
        No hay precios en los datos del proyecto; la suma de confianza no es un
        total a pagar.
      </p>
      {lineas.length === 0 && (
        <p className="estado-vacio">El carrito está vacío.</p>
      )}
      {lineas.length > 0 && (
        <>
          <button
            className="boton-vaciar"
            type="button"
            onClick={onVaciar}
          >
            Vaciar carrito
          </button>
          <ul className="carrito-lista">
            {lineas.map((linea) => (
              <li key={linea.id}>
                <div>
                  <strong>{linea.nombre}</strong>
                  <span>Confianza: {Number(linea.confianza).toFixed(2)}%</span>
                </div>
                <span className="carrito-cantidad">Cantidad: {linea.cantidad}</span>
                <button
                  className="boton-quitar"
                  type="button"
                  onClick={() => onQuitar(linea.id)}
                >
                  Quitar
                </button>
              </li>
            ))}
          </ul>
        </>
      )}
    </section>
  )
}

export default Carrito
