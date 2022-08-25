#Este import tendrá más sentido al hacer merge en la rama principal
from data.duenos import Dueno
import services.data_service as svc

active_account: Dueno = None


def reload_account():
    global active_account
    if not active_account:
        return

    active_account = svc.find_account_by_email(active_account.email)
