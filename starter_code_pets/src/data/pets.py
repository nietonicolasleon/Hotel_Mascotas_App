import datetime
import mongoengine as me

class Pet(me.Document):
    fecha_registro = me.DateTimeField(default=datetime.datetime.now())
    especie = me.StringField(required = True)
    raza = me.StringField()
    nombre = me.StringField(required = True)
    tamanio = me.FloatField(required = True)
    peso = me.FloatField(required = True)

    meta ={
        'db_alias' : 'core',
        'collection' : 'pets'
    }