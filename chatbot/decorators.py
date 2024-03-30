from chatbot.constants import LEVEL_ERROR, LEVEL_WARNING, GIVE_NAME_PHONE, GIVE_PHONE, GIVE_NAME, NOT_FOUND, \
    GIVE_NAME_OLD_PHONE_NEW_PHONE


def check_add_contacts_error(func):
    def inner(*args, **kwargs):
        try:
            if len(kwargs['args']) < 2:
                raise ValueError(LEVEL_ERROR + " " + GIVE_NAME_PHONE)

            return func(*args, **kwargs)

        except IndexError:
            raise ValueError(LEVEL_ERROR + " " + GIVE_NAME_PHONE)

    return inner


def check_show_phone_error(func):
    def inner(*args, **kwargs):
        try:
            if len(kwargs['args']) == 0 or str(kwargs['args'][0]).isalpha():
                raise ValueError(LEVEL_ERROR + " " + GIVE_PHONE)

            return func(*args, **kwargs)
        except IndexError:
            raise ValueError(LEVEL_ERROR + " " + GIVE_PHONE)

    return inner


def check_search_contact_error(func):
    def inner(*args, **kwargs):
        try:
            if len(kwargs['args']) == 0 or str(kwargs['args'][0]).isdigit():
                raise ValueError(LEVEL_ERROR + " " + GIVE_NAME)
            return func(*args, **kwargs)
        except IndexError:
            raise ValueError(LEVEL_ERROR + " " + GIVE_NAME)

    return inner


def check_empty_contacts_error(func):
    def inner(*args, **kwargs):
        if not len(kwargs['address_book']):
            raise ValueError(LEVEL_WARNING + " Contacts is empty now")
        return func(*args, **kwargs)

    return inner


def check_edit_phone_error(func):
    def inner(*args, **kwargs):
        try:
            if len(kwargs['args']) < 3:
                raise ValueError(LEVEL_ERROR + ' ' + GIVE_NAME_OLD_PHONE_NEW_PHONE)

            return func(*args, **kwargs)

        except IndexError:
            raise ValueError(LEVEL_ERROR + " " + NOT_FOUND)

    return inner


def check_delete_contact_error(func):
    def inner(*args, **kwargs):
        try:
            if len(kwargs['args']) == 0:
                raise ValueError(LEVEL_ERROR + ' ' + GIVE_NAME)

            return func(*args, **kwargs)
        except IndexError:
            raise ValueError(LEVEL_ERROR + " " + NOT_FOUND)

    return inner


def check_file_exists(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OSError:
            raise ValueError(LEVEL_ERROR + "Wrong path to file")

    return inner
