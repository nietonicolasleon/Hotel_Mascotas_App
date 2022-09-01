from infrastructure.switchlang import switch
import program_hosts as hosts
import infrastructure.state as state
import services.data_service as svc
from starter_code_pets.src.program_hosts import error_msg, success_msg
from dateutil import parser

def run():
    print(' ****************** Welcome guest **************** ')
    print()

    show_commands()

    while True:
        action = hosts.get_action()

        with switch(action) as s:
            s.case('c', hosts.create_account)
            s.case('l', hosts.log_into_account)

            s.case('a', add_a_snake)
            s.case('y', view_your_snakes)
            s.case('b', book_a_cage)
            s.case('v', view_bookings)
            s.case('m', lambda: 'change_mode')

            s.case('?', show_commands)
            s.case('', lambda: None)
            s.case(['x', 'bye', 'exit', 'exit()'], hosts.exit_app)

            s.default(hosts.unknown_command)

        state.reload_account()

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What action would you like to take:')
    print('[C]reate an account')
    print('[L]ogin to your account')
    print('[B]ook a cage')
    print('[A]dd a snake')
    print('View [y]our snakes')
    print('[V]iew your bookings')
    print('[M]ain menu')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


def add_a_snake():
    print(' ****************** Agregue una mascota **************** ')
    if not state.active_account:
        error_msg("Debe acceder a una cuenta primero para registrar una mascota.")
        return
    
    nombre = input("Ingrese el nombre de su mascota: ")
    if not nombre:
        error_msg("Operación cancelada")
        return
    
    especie = input("Ingrese la especie de su mascota: ")
    raza = input("Ingrese la raza de su mascota: ")
    tam = float(input("Ingrese el tamaño apróximado en metros de su mascota: "))
    peso = float(input("Ingrese el peso apróximado en kilos de su mascota: "))

    mascota = svc.add_pets(state.active_account, nombre, especie, raza, tam, peso)
    state.reload_account()

    success_msg("Se agregó la mascota: {}, con su id: {}".format(mascota.nombre, mascota.id))

def view_your_snakes():
    print(' ****************** Tus mascotas **************** ')
    if not state.active_account:
        error_msg("Debe acceder a una cuenta primero para ver sus mascota.")
        return
    
    mascotas = svc.get_pets_for_users(state.active_account.id)

    print("Usted tiene {} mascotas registradas".format(len(mascotas)))
    for m in mascotas:
        print(" * {} es un {} de la raza {}. Mide {} metros y pesa {} kilos.".format(
            m.nombre,
            m.especie,
            m.raza,
            m.tamanio,
            m.peso
        ))


def book_a_cage():
    print(' ****************** Book a cage **************** ')
    if not state.active_account:
        error_msg("Debe acceder a una cuenta primero para reservar una cucha.")
        return
    
    mascotas = svc.get_pets_for_users(state.active_account.id)
    if not mascotas:
        error_msg("Usted debe [a]ñadir una mascota primero.")
        return
    
    print("¡Busquemos una cucha libre para su mascota!")
    start_text = input("Ingrese la fecha del check-in [yyyy-mm-dd]: ")
    if not start_text:
        error_msg("Operación cancelada")
        return
    
    check_in = parser.parse(
        start_text
    )

    check_out = parser.parse(
        input("Ingrese la fecha del check-out [yyyy-mm-dd]:")
    )

    if check_in >= check_out:
        error_msg("La fecha de check in debe ser anterior a la de check out.")
        return
    


def view_bookings():
    print(' ****************** Your bookings **************** ')
    # TODO: Require an account
    # TODO: List booking info along with snake info

    print(" -------- NOT IMPLEMENTED -------- ")
