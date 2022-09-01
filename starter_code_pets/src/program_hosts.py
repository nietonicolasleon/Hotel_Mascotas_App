from ast import If
from re import S
from colorama import Fore
from infrastructure.switchlang import switch
import infrastructure.state as state
import services.data_service as svc
from dateutil import parser


def run():
    print(' ****************** Welcome host **************** ')
    print()

    show_commands()

    while True:
        action = get_action()

        with switch(action) as s:
            s.case('c', create_account)
            s.case('a', log_into_account)
            s.case('l', list_cages)
            s.case('r', register_cage)
            s.case('u', update_availability)
            s.case('v', view_bookings)
            s.case('m', lambda: 'change_mode')
            s.case(['x', 'bye', 'exit', 'exit()'], exit_app)
            s.case('?', show_commands)
            s.case('', lambda: None)
            s.default(unknown_command)

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What action would you like to take:')
    print('[C]reate an account')
    print('Login to your [a]ccount')
    print('[L]ist your cages')
    print('[R]egister a cage')
    print('[U]pdate cage availability')
    print('[V]iew your bookings')
    print('Change [M]ode (guest or host)')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


def create_account():
    print(' ****************** REGISTER **************** ')
    nombre = input("Ingrese su nombre, por favor: ")
    email = input("Ingrese su email, por favor: ").strip().lower()

    cuenta_vieja = svc.find_account_by_email(email)
    if cuenta_vieja:
        error_msg("Error: La cuenta con el email: {email} ya existe.")
        return

    state.active_account = svc.create_account(nombre, email)
    success_msg(f"Cuenta creada exitosamente con id: {state.active_account.id}.")


def log_into_account():
    print(' ****************** LOGIN **************** ')

    email = input("Ingrese su email, por favor: ").strip().lower()
    cuenta = svc.find_account_by_email(email)

    if not cuenta:
        error_msg(f"No se pudo encontrar la cuenta con el email: {email}.")
        return
    
    state.active_account = cuenta
    success_msg("Usted entró a su cuenta exitosamente.")


def register_cage():
    print(' ****************** REGISTER CAGE **************** ')
    if not state.active_account:
        error_msg('Debe acceder a una cuenta primero para registrar una cucha.')
        return
    
    metros = input('¿De cuantos metros cuadrados es la cucha? ')
    if not metros:
        error_msg('Registro cancelado.')
        return
    
    metros = float(metros)
    alfombra = input('¿La cucha tiene alfombra? [y, n] ').lower().startswith('y')
    juguetes = input('¿La cucha tiene juguetes? [y, n] ').lower().startswith('y')
    nombre = input('Dele un nombre a la cucha: ')
    precio = float(input('Dele un precio a la cucha por noche: '))

    cucha = svc.register_cage(
        state.active_account, nombre, juguetes, alfombra, metros, precio
    )

    state.reload_account()
    success_msg(f'Se registró una nueva cucha con la id: {cucha.id}.')


def list_cages(suppress_header=False):
    if not suppress_header:
        print(' ****************     Las Cuchas     **************** ')

    if not state.active_account:
        error_msg('Debe acceder a una cuenta primero para registrar una cucha.')
        return
    
    cuchas = svc.find_cucha_for_user(state.active_account)
    print(f'Usted tiene un total de {len(cuchas)} cuchas.')
    for idx, c in enumerate(cuchas):
        print(f' {idx + 1} {c.nombre} mide: {c.metros_cuadrados}.')
        for b in c.reservas:
            print('    * Reserva {}, {} días, reservado? {}'.format(
                b.fecha_check_in,
                (b.fecha_check_out - b.fecha_check_in).days,
                'YES' if b.fecha_reserva is not None else 'no'
            ))


def update_availability():
    print(' ****************** Add available date **************** ')
    if not state.active_account:
        error_msg("Debe acceder a una cuenta primero para registrar una cucha.")
        return
    
    list_cages(suppress_header=True)

    cage_number = input("Ingrese el número de la cucha a la que desea acceder: ")
    if not cage_number.strip():
        error_msg("Operación cancelada.")
        print()
        return
    
    cage_number = int(cage_number)

    cuchas = svc.find_cucha_for_user(state.active_account)
    selected_cage = cuchas[cage_number - 1]
    
    success_msg("Seleccionó la cucha {}".format(selected_cage.nombre))

    fecha_inicio = parser.parse(
        input("Ingrese una fecha real en el siguiente formato: [yyyy-mm-dd] (año, mes, dia)")
    )

    dias = int(input("Ingrese la cantidad de días de la reserva: "))

    
    state.reload_account()


def view_bookings():
    print(' ****************** Your bookings **************** ')

    # TODO: Require an account
    # TODO: Get cages, and nested bookings as flat list
    # TODO: Print details for each

    print(" -------- NOT IMPLEMENTED -------- ")


def exit_app():
    print()
    print('bye')
    raise KeyboardInterrupt()


def get_action():
    text = '> '
    if state.active_account:
        text = f'{state.active_account.nombre}> '

    action = input(Fore.YELLOW + text + Fore.WHITE)
    return action.strip().lower()


def unknown_command():
    print("Sorry we didn't understand that command.")


def success_msg(text):
    print(Fore.LIGHTGREEN_EX + text + Fore.WHITE)


def error_msg(text):
    print(Fore.LIGHTRED_EX + text + Fore.WHITE)
