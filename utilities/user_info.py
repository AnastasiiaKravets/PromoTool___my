import random

_TFS_user = "OFFICEUKRAINE\\an.kravets"
_TFS_password = "123Everybody"

_data_base_user = "OFFICEUKRAINE\\an.kravets"
_data_base_password = "123Everybody"


def get_new_user_name():
    randomizer = random.randint(1, 89405)

    return 'Autotest' + str(randomizer)