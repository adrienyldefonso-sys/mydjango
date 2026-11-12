export const productos = [
  { id: 7, nombre: 'Armazón Classic', tipo: 'armazon', marca: 'VisionPro', precio: '245.00', stock: 10 },
  { id: 9, nombre: 'Armazón Sport', tipo: 'armazon', marca: 'ActiveFit', precio: '260.00', stock: 7 },
  { id: 8, nombre: 'Lente Daily', tipo: 'lente_contacto', marca: 'ClearView', precio: '120.00', stock: 18 },
  { id: 12, nombre: 'Lente Daily Flex', tipo: 'lente_contacto', marca: 'Acuvue', precio: '60.00', stock: 40 },
  { id: 18, nombre: 'Lente Pro', tipo: 'luna', marca: 'Opti', precio: '150.00', stock: 12 },
]

export const clientesConVentas = [
  {
    id: 6,
    nombres: 'Ana',
    apellidos: 'García',
    ventas: [
      { id: 12, producto: 'Luna Blue', cantidad: 2, precio_unitario: '180.00' },
      { id: 13, producto: 'Armazón Classic', cantidad: 1, precio_unitario: '240.00' },
    ],
  },
  {
    id: 7,
    nombres: 'Luis',
    apellidos: 'Pérez',
    ventas: [
      { id: 10, producto: 'Lente Daily', cantidad: 2, precio_unitario: '120.00' },
    ],
  },
]
