class Pet:
    fecha_registro = None
    especie = None
    raza = None
    nombre = None
    tamanio = None
    peso = None

    meta ={
        'db_alias' : 'core',
        'collection' : 'pets'
    }