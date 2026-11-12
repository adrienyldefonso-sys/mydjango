function Tarjeta({ titulo, children }) {
  return (
    <section className="tarjeta">
      <h2 className="tarjeta-titulo">{titulo}</h2>
      <div className="tarjeta-contenido">{children}</div>
    </section>
  )
}

export default Tarjeta
