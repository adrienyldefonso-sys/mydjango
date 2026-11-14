function Buscador({ valor, onCambiar, filtroPlaga, onCambiarFiltro }) {
  return (
    <div className="filtros-diagnosticos">
      <label className="buscador-diagnosticos">
        Buscar diagnóstico
        <input
          type="search"
          value={valor}
          onChange={(evento) => onCambiar(evento.target.value)}
          placeholder="Busca por diagnóstico o código"
        />
      </label>
      <label className="buscador-diagnosticos">
        Filtrar por plaga
        <select
          value={filtroPlaga}
          onChange={(evento) => onCambiarFiltro(evento.target.value)}
        >
          <option value="">Todas las plagas</option>
          <option value="Potato___healthy">Saludable</option>
          <option value="Potato___Early_blight">Tizón Temprano</option>
          <option value="Potato___Late_blight">Tizón Tardío</option>
        </select>
      </label>
    </div>
  )
}

export default Buscador
