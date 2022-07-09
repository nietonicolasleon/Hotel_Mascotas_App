#Este import tendrá más sentido al hacer merge en la rama principal
from data.duenos import Dueno

active_account: Dueno = None


def reload_account():
    global active_account
    if not active_account:
        return

    # TODO: pull owner account from the database.
    pass
