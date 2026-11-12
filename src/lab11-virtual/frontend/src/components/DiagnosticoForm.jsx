import { useState } from 'react'

const TIPOS_PLAGA = [
  { codigo: 'Potato___healthy', nombre: 'Saludable' },
  { codigo: 'Potato___Early_blight', nombre: 'Tizón Temprano' },
  { codigo: 'Potato___Late_blight', nombre: 'Tizón Tardío' },
]

function DiagnosticoForm({ parcelaId, onGuardar }) {
  const [plagaDetectada, setPlagaDetectada] = useState('')
  const [fechaCaptura, setFechaCaptura] = useState('')
  const [confianza, setConfianza] = useState('')
  const [imagenUrl, setImagenUrl] = useState('')
  const [error, setError] = useState('')
  const [mensaje, setMensaje] = useState('')

  function enviar(evento) {
    evento.preventDefault()
    setError('')
    setMensaje('')

    // El modelo de la API requiere parcela, fecha y campos de plaga.
    if (!plagaDetectada) {
      setError('Selecciona el diagnóstico que deseas registrar.')
      return
    }

    if (!fechaCaptura || Number.isNaN(new Date(fechaCaptura).getTime())) {
      setError('La fecha y hora son obligatorias y deben ser válidas.')
      return
    }

    if (confianza.trim() === '') {
      setError('La confianza es obligatoria.')
      return
    }

    // La API valida confianza entre 0 y 100, con hasta dos decimales.
    const confianzaNumero = Number(confianza)
    const decimalesConfianza = confianza.includes('.')
      ? confianza.split('.')[1]
      : ''
    if (
      !Number.isFinite(confianzaNumero)
      || confianzaNumero < 0
      || confianzaNumero > 100
      || decimalesConfianza.length > 2
    ) {
      setError('La confianza debe ser un número entre 0 y 100, con máximo dos decimales.')
      return
    }

    if (imagenUrl.trim()) {
      try {
        const url = new URL(imagenUrl.trim())
        if (!['http:', 'https:'].includes(url.protocol)) {
          setError('La imagen debe usar una URL HTTP o HTTPS.')
          return
        }
      } catch {
        setError('Ingresa una URL de imagen válida.')
        return
      }
    }

    const tipo = TIPOS_PLAGA.find((item) => item.codigo === plagaDetectada)
    if (!tipo) {
      setError('Selecciona un diagnóstico válido.')
      return
    }

    // onGuardar envía el nuevo objeto al padre; el formulario no modifica su lista.
    onGuardar({
      id: crypto.randomUUID(),
      parcela: parcelaId,
      fecha_captura: new Date(fechaCaptura).toISOString(),
      plaga_detectada: tipo.codigo,
      plaga_nombre: tipo.nombre,
      confianza: confianzaNumero.toFixed(2),
      imagen_url: imagenUrl.trim(),
    })

    setPlagaDetectada('')
    setFechaCaptura('')
    setConfianza('')
    setImagenUrl('')
    setMensaje('Diagnóstico agregado al historial de esta parcela.')
  }

  return (
    <form className="diagnostico-form" noValidate onSubmit={enviar}>
      <h3>Agregar diagnóstico de prueba</h3>
      <div className="diagnostico-form-grid">
        <label>
          Plaga detectada
          <select
            required
            value={plagaDetectada}
            onChange={(evento) => setPlagaDetectada(evento.target.value)}
          >
            <option value="">Selecciona un diagnóstico</option>
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
            min="0"
            max="100"
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
