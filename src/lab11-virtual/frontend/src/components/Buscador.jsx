function Buscador({ valor, onCambiar }) {
  return (
    <label className="buscador-diagnosticos">
      Buscar diagnóstico
      {/* El padre controla valor y recibe cada cambio para filtrar el listado. */}
      <input
        type="search"
        value={valor}
        onChange={(evento) => onCambiar(evento.target.value)}
        placeholder="Busca por diagnóstico o código"
      />
    </label>
  )
}

export default Buscador
