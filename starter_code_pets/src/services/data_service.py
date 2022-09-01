#Este import tendrá más sentido al hacer merge en la rama principal
import datetime
from typing import List
from data.duenos import Dueno
from data.cuchas import Cucha
from data.reservas import Reserva

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


def add_available_date(cucha_elegida: Cucha, fecha_ini: datetime.datetime, dias: int):
    reserva = Reserva()
    reserva.fecha_check_in = fecha_ini
    reserva.fecha_check_out = datetime.timedelta(days=dias)
    cucha_elegida = Cucha.objects(id = cucha_elegida.id).first()
    cucha_elegida.reservas.append(reserva)
    cucha_elegida.save()
    return cucha_elegida