#Este import tendrá más sentido al hacer merge en la rama principal
from data.duenos import Dueno
from data.cuchas import Cucha

def create_account(nombre: str, email: str) -> Dueno:
    owner = Dueno()
    owner.nombre = nombre
    owner.email = email

    owner.save()

    return owner

def find_account_by_email(email: str) -> Dueno:

    owner = Dueno.objects(email = email).first()
    return owner

def register_cage(active_account: Dueno, nombre, juguetes, alfombra, metros) -> Cucha:
    cucha = Cucha()

    cucha.nombre = nombre
    cucha.tiene_juguetes = juguetes
    cucha.tiene_alfombra = alfombra
    cucha.metros_cuadrados = metros

    cucha.save()

    cuenta = find_account_by_email(active_account.email)
    cuenta.cucha_ids.append(cucha.id)
    cucha.save()
    
    return cucha