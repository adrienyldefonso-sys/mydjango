import { useEffect } from 'react'

function Aviso({ aviso, onCerrar }) {
  useEffect(() => {
    if (!aviso) {
      return undefined
    }

    // Cancela el aviso anterior si llega uno nuevo o se desmonta el componente.
    const temporizador = setTimeout(onCerrar, 3000)
    return () => clearTimeout(temporizador)
  }, [aviso, onCerrar])

  if (!aviso) {
    return null
  }

  return (
    <p className="aviso" role="status">
      Agregado: {aviso.nombre}
    </p>
  )
}

export default Aviso
