import { useState } from 'react'

function DiagnosticoCard({
  diagnostico,
  mostrarFecha = true,
  onAgregar,
  onEliminar,
  onCambiarEstado,
}) {
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
        <span className={`estado-registro ${diagnostico.activo ? 'activo' : 'inactivo'}`}>
          {diagnostico.activo ? 'Activo' : 'Inactivo'}
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
        <button
          className="boton-agregar"
          type="button"
          onClick={() => onAgregar(diagnostico)}
        >
          Agregar
        </button>
        {/* Estos controles solo notifican al padre; no cambian la prop diagnostico. */}
        <button
          className="boton-imagen"
          type="button"
          onClick={() => onCambiarEstado(diagnostico.id)}
        >
          {diagnostico.activo ? 'Desactivar' : 'Activar'}
        </button>
        <button
          className="boton-eliminar"
          type="button"
          onClick={() => onEliminar(diagnostico.id)}
        >
          Eliminar
        </button>
      </div>
    </article>
  )
}

export default DiagnosticoCard
