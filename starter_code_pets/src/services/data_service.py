#Este import tendrá más sentido al hacer merge en la rama principal
from typing import List
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


def register_cage(active_account: Dueno, nombre, juguetes, alfombra, metros, precio) -> Cucha:
    cucha = Cucha()

    cucha.nombre = nombre
    cucha.tiene_juguetes = juguetes
    cucha.tiene_alfombra = alfombra
    cucha.metros_cuadrados = metros
    cucha.precio = precio

    cucha.save()

    cuenta = find_account_by_email(active_account.email)
    cuenta.cucha_ids.append(cucha.id)
    cuenta.save()

    return cucha


def find_cucha_for_user(account: Dueno) -> List[Cucha]:
    query = Cucha.objects(id__in = account.cucha_ids)
    cuchas = list(query)
    return cuchas