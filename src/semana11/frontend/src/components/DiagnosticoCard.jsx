import { useState } from 'react'

function DiagnosticoCard({ diagnostico, mostrarFecha = true }) {
  const [imagenVisible, setImagenVisible] = useState(false)
  const confianza = Number(diagnostico.confianza)

  return (
    <article className="diagnostico-card">
      {diagnostico.imagen_url && imagenVisible && (
        <img
          className="diagnostico-imagen"
          src={diagnostico.imagen_url}
          alt={`Imagen del diagnóstico: ${diagnostico.plaga_nombre}`}
          loading="lazy"
        />
      )}
      <div className="diagnostico-info">
        <span className={`estado-pill ${diagnostico.plaga_detectada.endsWith('healthy') ? 'saludable' : 'alerta'}`}>
          {diagnostico.plaga_nombre}
        </span>
        {mostrarFecha && (
          <time dateTime={diagnostico.fecha_captura}>
            {new Intl.DateTimeFormat('es-PE', {
              dateStyle: 'medium',
              timeStyle: 'short',
            }).format(new Date(diagnostico.fecha_captura))}
          </time>
        )}
        <p>Confianza: <strong>{confianza.toFixed(2)}%</strong></p>
        <small>{diagnostico.plaga_detectada}</small>
        {diagnostico.imagen_url && (
          <button
            className="boton-imagen"
            type="button"
            aria-expanded={imagenVisible}
            onClick={() => setImagenVisible((visible) => !visible)}
          >
            {imagenVisible ? 'Ocultar imagen' : 'Ver imagen'}
          </button>
        )}
      </div>
    </article>
  )
}

export default DiagnosticoCard
