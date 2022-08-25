import mongoengine

def global_init():
    mongoengine.connect(db='hotel_mascotas', host='mongodb+srv://MarisaF:trumpe2020@cluster0.zax8qxg.mongodb.net/?retryWrites=true&w=majority', alias='core')