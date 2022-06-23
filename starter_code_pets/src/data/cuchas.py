import datetime
import mongoengine as me
from data.reservas import Reserva

class Cucha(me.Document):
    fecha_registro = me.DateTimeField(default=datetime.datetime.now())
    nombre = me.StringField(required=True)
    precio = me.FloatField(required = True)
    metros_cuadrados = me.FloatField(required = True)
    tiene_alfombra = me.BooleanField(required = True)
    tiene_juguetes = me.BooleanField(required = True)

    reservas = me.EmbeddedDocumentListField(Reserva)

    meta ={
        'db_alias' : 'core',
        'collection' : 'cuchas'
    }