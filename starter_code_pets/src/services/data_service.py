#Este import tendrá más sentido al hacer merge en la rama principal
from data.duenos import Dueno

def create_account(nombre: str, email: str) -> Dueno:
    owner = Dueno()
    owner.nombre = nombre
    owner.email = email

    owner.save()

    return owner

def find_account_by_email(email: str) -> Dueno:

    owner = Dueno.objects(email = email).first()
    return owner