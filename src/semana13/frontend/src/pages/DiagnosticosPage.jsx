import { useEffect, useState } from 'react'
import api from '../api'
import DiagnosticoCard from '../components/DiagnosticoCard'

function DiagnosticosPage() {
  const [diagnosticos, setDiagnosticos] = useState([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let activo = true

    async function cargarDiagnosticos() {
      try {
        const respuesta = await api.get('diagnosticos/')
        if (activo) {
          setDiagnosticos(respuesta.data)
        }
      } catch (errorPeticion) {
        console.error('No se pudieron cargar los diagnósticos.', errorPeticion)
        if (activo) {
          setError('No se pudieron cargar los diagnósticos.')
        }
      } finally {
        if (activo) {
          setCargando(false)
        }
      }
    }

    cargarDiagnosticos()
    return () => {
      activo = false
    }
  }, [])

  return (
    <main>
      <h1>Diagnósticos de Ojo d’Chakra</h1>
      {cargando && <p role="status">Cargando diagnósticos...</p>}
      {error && <p role="alert">{error}</p>}
      {!cargando && !error && diagnosticos.length === 0 && (
        <p>No hay diagnósticos registrados.</p>
      )}
      {!error && diagnosticos.map((diagnostico) => (
        <DiagnosticoCard key={diagnostico.id} diagnostico={diagnostico} />
      ))}
    </main>
  )
}

export default DiagnosticosPage