import datetime
from typing import List
import bson
from data.duenos import Dueno
from data.cuchas import Cucha
from data.reservas import Reserva
from data.pets import Pet

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


def add_pets(account, n, e, r, t, p) -> Pet:
    dueno = find_account_by_email(account.email)
    mascota = Pet()
    mascota.nombre = n
    mascota.especie = e
    mascota.raza = r
    mascota.tamanio = t
    mascota.peso = p

    mascota.save()
    dueno.pet_ids.append(mascota.id)
    dueno.save()

    return mascota


def get_pets_for_users(user_id: bson.ObjectId) -> List[Pet]:
    dueno = Dueno.objects(id = user_id).first()
    mascotas = Pet.object(id__in = dueno.pet_ids).all()

    return list(mascotas)


def get_available_cages(ci: datetime.datetime, co: datetime.datetime, m: Pet) -> Cucha:
    tam_min = m.tamanio * 1.5

    query = Cucha.objects() \
        .filter(metros_cuadrados__gte = tam_min) \
        .filter(reservas__fecha_check_in__lte = ci) \
        .filter(reservas__fecha_check_out__lte = co)
    
    cuchas = query.order_by('precio')

    cuchas_finale = []
    for c in cuchas:
        for r in c.reservas:
            if r.fecha_check_in <= ci and r.fecha_check_out >= co and r.guest_pet_id is None:
                cuchas_finale.append(c)
    
    return cuchas_finale


def book_cucha(account, mascota, cucha, ci, co):
    reserva = None

    for r in cucha.reservas:
        if r.fecha_check_in <= ci and r.fecha_check_out >= co and r.guest_pet_id is None:
            reserva = r
            break
    
    reserva.guest_dueno_id = account.id
    reserva.guest_pet_id = mascota.id
    reserva.fecha_reserva = datetime.datetime.now()

    cucha.save()
