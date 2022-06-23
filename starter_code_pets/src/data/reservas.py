import mongoengine as me

class Reserva(me.EmbeddedDocument):
    guest_dueno_id = me.ObjectIdField()
    guest_pet_id = me.ObjectIdField()
    fecha_reserva = me.DateTimeField()
    fecha_check_in = me.DateTimeField(required = True)
    fecha_check_out = me.DateTimeField(required = True)
    review = me.StringField()
    rating = me.IntField(default = 0)