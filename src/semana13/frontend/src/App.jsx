import { Navigate, Route, Routes } from 'react-router-dom'
import DiagnosticosPage from './pages/DiagnosticosPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/diagnosticos" replace />} />
      <Route path="/diagnosticos" element={<DiagnosticosPage />} />
      <Route path="*" element={<main><h1>Página no encontrada</h1></main>} />
    </Routes>
  )
}

export default App
