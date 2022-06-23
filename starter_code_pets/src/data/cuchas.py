class Cucha:
    fecha_registro = None
    nombre = None
    precio = None
    metros_cuadrados = None
    tiene_alfombra = None
    tiene_juguetes = None

    reservas = list()

    meta ={
        'db_alias' : 'core',
        'collection' : 'cuchas'
    }