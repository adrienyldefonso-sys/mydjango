import { useState } from 'react'

const TIPOS_PLAGA = [
  { codigo: 'Potato___healthy', nombre: 'Saludable' },
  { codigo: 'Potato___Early_blight', nombre: 'Tizón Temprano' },
  { codigo: 'Potato___Late_blight', nombre: 'Tizón Tardío' },
]

function DiagnosticoForm({ parcelaId, onAgregar }) {
  const [plagaDetectada, setPlagaDetectada] = useState(TIPOS_PLAGA[0].codigo)
  const [fechaCaptura, setFechaCaptura] = useState('')
  const [confianza, setConfianza] = useState('')
  const [imagenUrl, setImagenUrl] = useState('')
  const [error, setError] = useState('')
  const [mensaje, setMensaje] = useState('')

  function enviar(evento) {
    evento.preventDefault()
    setError('')
    setMensaje('')

    const confianzaNumero = Number(confianza)
    if (!Number.isFinite(confianzaNumero) || confianzaNumero < 0 || confianzaNumero > 100) {
      setError('La confianza debe estar entre 0 y 100.')
      return
    }

    if (!fechaCaptura || Number.isNaN(new Date(fechaCaptura).getTime())) {
      setError('Ingresa una fecha y hora válidas.')
      return
    }

    const tipo = TIPOS_PLAGA.find((item) => item.codigo === plagaDetectada)
    onAgregar({
      id: crypto.randomUUID(),
      parcela: parcelaId,
      fecha_captura: new Date(fechaCaptura).toISOString(),
      plaga_detectada: tipo.codigo,
      plaga_nombre: tipo.nombre,
      confianza: Number(confianzaNumero.toFixed(2)),
      imagen_url: imagenUrl.trim(),
    })

    setFechaCaptura('')
    setConfianza('')
    setImagenUrl('')
    setMensaje('Diagnóstico agregado al historial de esta parcela.')
  }

  return (
    <form className="diagnostico-form" onSubmit={enviar}>
      <h3>Agregar diagnóstico de prueba</h3>
      <div className="diagnostico-form-grid">
        <label>
          Plaga detectada
          <select
            value={plagaDetectada}
            onChange={(evento) => setPlagaDetectada(evento.target.value)}
          >
            {TIPOS_PLAGA.map((tipo) => (
              <option key={tipo.codigo} value={tipo.codigo}>{tipo.nombre}</option>
            ))}
          </select>
        </label>
        <label>
          Fecha y hora
          <input
            type="datetime-local"
            required
            value={fechaCaptura}
            onChange={(evento) => setFechaCaptura(evento.target.value)}
          />
        </label>
        <label>
          Confianza (%)
          <input
            type="number"
            step="0.01"
            required
            value={confianza}
            onChange={(evento) => setConfianza(evento.target.value)}
          />
        </label>
        <label>
          URL de imagen (opcional)
          <input
            type="url"
            value={imagenUrl}
            onChange={(evento) => setImagenUrl(evento.target.value)}
            placeholder="https://ejemplo.com/hoja.jpg"
          />
        </label>
      </div>
      <button className="boton-agregar" type="submit">Agregar al historial</button>
      {error && <p className="form-feedback error" role="alert">{error}</p>}
      {mensaje && <p className="form-feedback success" role="status">{mensaje}</p>}
    </form>
  )
}

export default DiagnosticoForm
