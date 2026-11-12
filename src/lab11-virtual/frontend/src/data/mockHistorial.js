export const mockHistorialData = {
  parcela: {
    id: '0f56200f4b594830b94a685c14b0143c',
    nombre: 'Chacra Los Andes',
    cultivo: 'Papa',
    referencia: 'Huarochirí',
    latitud: '-12.13',
    longitud: '-76.23',
    agricultor: 'Luis Quispe',
    total_diagnosticos: 5,
  },
  resumen: {
    total: 5,
    ultima_fecha: '2026-10-30T16:36:38.021716-05:00',
    por_plaga: {
      Potato___Early_blight: 1,
      Potato___Late_blight: 2,
      Potato___healthy: 2,
    },
  },
  diagnosticos: [
    {
      id: 'd3257ceb3cf5448eaee151c8654b8879',
      fecha_captura: '2026-10-30T16:36:38.021716-05:00',
      plaga_detectada: 'Potato___healthy',
      plaga_nombre: 'Saludable',
      confianza: '98.50',
      imagen_url: 'https://via.placeholder.com/150',
    },
    {
      id: 'a1127ceb3cf5448eaee151c8654b8812',
      fecha_captura: '2026-10-28T10:15:00.000000-05:00',
      plaga_detectada: 'Potato___Late_blight',
      plaga_nombre: 'Tizón Tardío',
      confianza: '92.10',
      imagen_url: 'https://via.placeholder.com/150',
    },
    {
      id: 'b2237ceb3cf5448eaee151c8654b8834',
      fecha_captura: '2026-10-25T14:22:10.000000-05:00',
      plaga_detectada: 'Potato___Early_blight',
      plaga_nombre: 'Tizón Temprano',
      confianza: '85.40',
      imagen_url: 'https://via.placeholder.com/150',
    },
    {
      id: 'c3348dcb9ad64834a976e3d02d88d120',
      fecha_captura: '2026-10-23T12:08:00.000000-05:00',
      plaga_detectada: 'Potato___Late_blight',
      plaga_nombre: 'Tizón Tardío',
      confianza: '88.30',
      imagen_url: 'https://via.placeholder.com/150',
    },
    {
      id: 'e5569eec1b9c4aa7a380e4d7719bc541',
      fecha_captura: '2026-10-20T09:45:00.000000-05:00',
      plaga_detectada: 'Potato___healthy',
      plaga_nombre: 'Saludable',
      confianza: '96.20',
      imagen_url: 'https://via.placeholder.com/150',
    },
  ],
}

export const parcelasMock = [mockHistorialData]
