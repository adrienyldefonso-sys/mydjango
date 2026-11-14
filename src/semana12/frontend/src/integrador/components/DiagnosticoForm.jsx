import { useState } from 'react'

const TIPOS_PLAGA = [
  { codigo: 'Potato___healthy', nombre: 'Saludable' },
  { codigo: 'Potato___Early_blight', nombre: 'Tizón Temprano' },
  { codigo: 'Potato___Late_blight', nombre: 'Tizón Tardío' },
]

function convertirFechaLocal(fecha) {
  if (!fecha) {
    return ''
  }

  const valor = new Date(fecha)
  if (Number.isNaN(valor.getTime())) {
    return ''
  }

  const horaLocal = new Date(
    valor.getTime() - valor.getTimezoneOffset() * 60000,
  )
  return horaLocal.toISOString().slice(0, 16)
}

function DiagnosticoForm({
  parcelaId,
  diagnostico,
  errorServidor,
  mensaje,
  guardando,
  onGuardar,
  onCancelar,
}) {
  const [plagaDetectada, setPlagaDetectada] = useState(
    diagnostico?.plaga_detectada ?? '',
  )
  const [fechaCaptura, setFechaCaptura] = useState(
    convertirFechaLocal(diagnostico?.fecha_captura),
  )
  const [confianza, setConfianza] = useState(
    diagnostico ? String(diagnostico.confianza) : '',
  )
  const [imagenUrl, setImagenUrl] = useState(diagnostico?.imagen_url ?? '')
  const [errorLocal, setErrorLocal] = useState('')

  async function enviar(evento) {
    evento.preventDefault()
    setErrorLocal('')

    if (!plagaDetectada || !fechaCaptura || confianza.trim() === '') {
      setErrorLocal('Completa el diagnóstico, la fecha y la confianza.')
      return
    }

    const confianzaNumero = Number(confianza)
    if (!Number.isFinite(confianzaNumero)) {
      setErrorLocal('La confianza debe ser un número.')
      return
    }

    const tipo = TIPOS_PLAGA.find((item) => item.codigo === plagaDetectada)
    if (!tipo) {
      setErrorLocal('Selecciona un diagnóstico válido.')
      return
    }

    const datos = {
      parcela: parcelaId,
      fecha_captura: new Date(fechaCaptura).toISOString(),
      plaga_detectada: tipo.codigo,
      plaga_nombre: tipo.nombre,
      confianza,
      imagen_url: imagenUrl.trim(),
    }

    const guardado = await onGuardar(datos)
    if (guardado && !diagnostico) {
      setPlagaDetectada('')
      setFechaCaptura('')
      setConfianza('')
      setImagenUrl('')
    }
  }

  return (
    <form className="diagnostico-form" noValidate onSubmit={enviar}>
      <h3>{diagnostico ? 'Editar diagnóstico' : 'Agregar diagnóstico'}</h3>
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
      <div className="form-actions">
        <button className="boton-agregar" type="submit" disabled={guardando}>
          {guardando ? 'Guardando...' : diagnostico ? 'Guardar cambios' : 'Crear diagnóstico'}
        </button>
        {diagnostico && (
          <button
            className="boton-imagen"
            type="button"
            disabled={guardando}
            onClick={onCancelar}
          >
            Cancelar edición
          </button>
        )}
      </div>
      {errorLocal && <p className="form-feedback error" role="alert">{errorLocal}</p>}
      {errorServidor && (
        <div className="form-feedback error" role="alert">
          <p>El servidor rechazó los datos:</p>
          <pre>{JSON.stringify(errorServidor, null, 2)}</pre>
        </div>
      )}
      {mensaje && <p className="form-feedback success" role="status">{mensaje}</p>}
    </form>
  )
}

export default DiagnosticoForm
