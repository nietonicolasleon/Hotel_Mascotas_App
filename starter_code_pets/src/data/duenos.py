import datetime
import mongoengine as me

class Dueno(me.Document):
    fecha_registro = me.DateTimeField(default=datetime.datetime.now())
    nombre = me.StringField(required=True)
    email = me.StringField(required=True)
    
    pet_ids = me.ListField()
    cucha_ids = me.ListField()

    meta ={
        'db_alias' : 'core',
        'collection' : 'duenos'
    }