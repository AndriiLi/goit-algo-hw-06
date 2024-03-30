from pathlib import Path

from chatbot.classes import AddressBook, Record, Name, Phone
from chatbot.command_parser import read_file
from chatbot.constants import DB_PATH, LEVEL_WARNING
from chatbot.decorators import check_edit_phone_error, \
    check_empty_contacts_error, check_file_exists, check_add_contacts_error, check_show_phone_error, \
    check_delete_contact_error, check_search_contact_error


@check_add_contacts_error
def add_contact(args: tuple[str, str], address_book: AddressBook) -> str:
    record = Record(args[0].strip())
    phone = args[1].strip()

    if address_book.find_record_by_name(record.name.value):
        raise ValueError(LEVEL_WARNING + ' Contact is already exists')

    record.add_phone(phone)
    address_book.add_record(record)
    return "Contact added."


@check_empty_contacts_error
def all_contacts(address_book: AddressBook) -> str:
    return address_book.print_all() if len(address_book) else 'Address book is empty'


@check_search_contact_error
def find_contact_by_name(args: tuple[str], address_book: AddressBook) -> str:
    name = args[0].strip().capitalize()
    record = address_book.find_record_by_name(name)
    return f"{record.name} phone(s): [ {record.get_phones()} ]"


@check_show_phone_error
def find_contact_by_phone(args: tuple[str], address_book: AddressBook) -> str:
    phone = args[0].strip()
    record = address_book.find_record_by_phone(phone)
    return f"{record.name} phone(s): [ {record.get_phones()} ]"


@check_delete_contact_error
def delete_contact(args: tuple[str], address_book: AddressBook) -> str:
    name = args[0].strip()
    address_book.delete_record(name)
    return "Contact has been deleted."


@check_edit_phone_error
def change_phone(args: tuple[str, str, str], address_book: AddressBook) -> str:
    name = args[0].strip()
    record = address_book.find_record_by_name(name)
    record.edit_phone(args[1].strip(), args[2].strip())

    return "Contact updated."


@check_add_contacts_error
def add_phone(args: tuple[str, str], address_book: AddressBook) -> str:
    name = args[0].strip()
    phone = args[1].strip()
    record = address_book.find_record_by_name(name)

    if not record:
        raise ValueError(LEVEL_WARNING + " Contact doesn't exists, add contact before")

    if record.is_exists(Phone(phone)):
        raise ValueError(LEVEL_WARNING + ' Contact already has this phone number')

    record.add_phone(phone)
    return "Phone added."


@check_add_contacts_error
def del_phone(args: tuple[str, str], address_book: AddressBook) -> str:
    name = Name(args[0].strip())
    phone = Phone(args[1].strip())
    record = address_book.find_record_by_name(name.value)

    if record.is_exists(phone) is False:
        raise ValueError(LEVEL_WARNING + " Contact doesn't have this phone number")

    record.remove_phone(phone)
    address_book.data[name.value] = record
    return "Phone deleted."


@check_file_exists
def export_contacts(address_book: AddressBook) -> str:
    with open(Path(DB_PATH).absolute(), 'w') as f:
        for record in address_book.values():
            f.write(f"{record.name.value} {record.get_phones(' ')}\n")

    return "Contacts saved into file."


@check_file_exists
def import_contacts(address_book: AddressBook) -> str:
    for row in read_file(Path(DB_PATH).absolute()):
        r = row.split(' ')
        name = r[0].strip()
        record = Record(name)
        for phone in r[1:]:
            record.add_phone(phone)

        address_book.add_record(record)

    return "Contacts loaded from file."
