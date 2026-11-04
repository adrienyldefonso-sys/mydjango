export const mockHistorialData = {
  parcela: {
    id: '0f56200f4b594830b94a685c14b0143c',
    nombre: 'Chacra Los Andes',
    cultivo: 'Papa',
    referencia: 'Huarochirí',
    latitud: -12.13,
    longitud: -76.23,
    agricultor: 'Luis Quispe',
    total_diagnosticos: 6,
  },
  resumen: {
    total: 6,
    ultima_fecha: '2026-10-30T16:36:38.021716-05:00',
    por_plaga: {
      Potato___Early_blight: 1,
      Potato___Late_blight: 3,
      Potato___healthy: 2,
    },
  },
  diagnosticos: [
    {
      id: 'd3257ceb3cf5448eaee151c8654b8879',
      fecha_captura: '2026-10-30T16:36:38.021716-05:00',
      plaga_detectada: 'Potato___healthy',
      plaga_nombre: 'Saludable',
      confianza: 98.5,
      imagen_url: 'https://via.placeholder.com/150',
    },
    {
      id: 'a1127ceb3cf5448eaee151c8654b8812',
      fecha_captura: '2026-10-28T10:15:00.000000-05:00',
      plaga_detectada: 'Potato___Late_blight',
      plaga_nombre: 'Tizón Tardío',
      confianza: 92.1,
      imagen_url: 'https://via.placeholder.com/150',
    },
    {
      id: 'b2237ceb3cf5448eaee151c8654b8834',
      fecha_captura: '2026-10-25T14:22:10.000000-05:00',
      plaga_detectada: 'Potato___Early_blight',
      plaga_nombre: 'Tizón Temprano',
      confianza: 85.4,
      imagen_url: 'https://via.placeholder.com/150',
    },
  ],
}

export const parcelasMock = [mockHistorialData]
