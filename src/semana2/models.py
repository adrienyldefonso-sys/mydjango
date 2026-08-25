# Datos en memoria para objetos encontrados
# NO se utiliza base de datos para esta funcionalidad

objetos_encontrados = [
    {
        "id": 1,
        "nombre": "Mochila negra",
        "descripcion": "Mochila negra con cuadernos y bolígrafos",
        "ubicacion": "Biblioteca",
        "fecha": "25/08/2026",
        "contacto": "Ana Torres"
    },
    {
        "id": 2,
        "nombre": "Lentes de sol",
        "descripcion": "Lentes de sol con marco dorado",
        "ubicacion": "Patio principal",
        "fecha": "24/08/2026",
        "contacto": "Carlos Mendez"
    },
    {
        "id": 3,
        "nombre": "Tarjeta de estudiante",
        "descripcion": "Tarjeta de identificación con código de barras",
        "ubicacion": "Cafetería",
        "fecha": "23/08/2026",
        "contacto": "María García"
    },
    {
        "id": 4,
        "nombre": "Llaves",
        "descripcion": "Manojo de llaves con llavero de color rojo",
        "ubicacion": "Sala de informática",
        "fecha": "22/08/2026",
        "contacto": "Pedro Rodríguez"
    },
    {
        "id": 5,
        "nombre": "Auriculares",
        "descripcion": "Auriculares inalámbricos color blanco",
        "ubicacion": "Aula 305",
        "fecha": "21/08/2026",
        "contacto": "Laura López"
    },
    {
        "id": 6,
        "nombre": "Cartera de cuero marrón",
        "descripcion": "Cartera marrón con documentos de identidad",
        "ubicacion": "Biblioteca - Segundo piso",
        "fecha": "20/08/2026",
        "contacto": "Juan Pérez - 3012345678"
    },
    {
        "id": 7,
        "nombre": "Cuaderno rojo",
        "descripcion": "Cuaderno de 100 hojas, color rojo con líneas",
        "ubicacion": "Aula 102",
        "fecha": "19/08/2026",
        "contacto": "Sofia Ruiz"
    },
    {
        "id": 8,
        "nombre": "Teléfono móvil",
        "descripcion": "Teléfono Samsung color negro con funda azul",
        "ubicacion": "Patio principal",
        "fecha": "18/08/2026",
        "contacto": "Diego Martínez - diego@email.com"
    },
    {
        "id": 9,
        "nombre": "Reloj de pulsera",
        "descripcion": "Reloj de pulsera con correa de cuero negro",
        "ubicacion": "Cafetería",
        "fecha": "17/08/2026",
        "contacto": "Isabela Corrales"
    },
    {
        "id": 10,
        "nombre": "Botella de agua",
        "descripcion": "Botella térmica roja con diseño de flores",
        "ubicacion": "Cancha de deportes",
        "fecha": "16/08/2026",
        "contacto": "Miguel Henao - 3019876543"
    },
]


def obtener_objetos():
    """Retorna la lista de objetos encontrados"""
    return objetos_encontrados


def obtener_objeto_por_id(objeto_id):
    """Obtiene un objeto por su ID"""
    for objeto in objetos_encontrados:
        if objeto['id'] == objeto_id:
            return objeto
    return None


def agregar_objeto(nombre, descripcion, ubicacion, fecha, contacto):
    """Agrega un nuevo objeto a la lista"""
    nuevo_id = max([obj['id'] for obj in objetos_encontrados], default=0) + 1
    nuevo_objeto = {
        "id": nuevo_id,
        "nombre": nombre,
        "descripcion": descripcion,
        "ubicacion": ubicacion,
        "fecha": fecha,
        "contacto": contacto
    }
    objetos_encontrados.append(nuevo_objeto)
    return nuevo_objeto


def buscar_objetos(termino):
    """
    Busca objetos por nombre o ubicación (búsqueda case-insensitive)
    Retorna lista de objetos que coinciden
    """
    if not termino or not termino.strip():
        return obtener_objetos()
    
    termino_lower = termino.lower().strip()
    resultados = []
    
    for objeto in objetos_encontrados:
        # Busca en nombre o ubicación
        if (termino_lower in objeto['nombre'].lower() or 
            termino_lower in objeto['ubicacion'].lower()):
            resultados.append(objeto)
    
    return resultados
