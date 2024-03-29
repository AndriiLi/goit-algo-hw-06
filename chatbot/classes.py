import re
from collections import UserDict
from typing import Tuple, Any

from chatbot.constants import LEVEL_WARNING, PHONE_WRONG_FORMAT, LEVEL_ERROR, NOT_FOUND, GIVE_PHONE


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return self.value


class Name(Field):
    def __init__(self, name: str):
        super().__init__(name.capitalize())


class Phone(Field):
    def __init__(self, phone: str):
        if self.is_valid_phone(phone):
            super().__init__(self.format_phone(phone))
        else:
            raise ValueError(LEVEL_ERROR + ' ' + PHONE_WRONG_FORMAT)

    def is_valid_phone(self, phone: str) -> bool:
        pattern = r"(^\+38\d{10}$)|(^\d{10}$)"
        if re.search(pattern, phone):
            return True

        return False

    def format_phone(self, phone: str) -> str:
        if not phone.startswith('+38'):
            phone = f"+38{phone}"

        return phone


class Record:
    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: list[Phone] = []

    def get_phone_index(self, phone) -> int | None:
        search = Phone(phone)
        for idx, p in enumerate(self.phones):
            if p.value == search.value:
                return idx
        return None

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        self.phones = [Phone(p) for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        index = self.get_phone_index(old_phone)
        if index is None:
            raise ValueError(f"{LEVEL_WARNING} Contact doesn't have phone number {old_phone},"
                             f" now this changing is impossible, "
                             f" input valid number which you want change")

        self.phones[index] = Phone(new_phone)

    def get_phones(self, separator: str = ', ') -> str:
        return separator.join(p.value for p in self.phones)

    def __str__(self) -> str:
        return f"Contact name: {self.name.value} phones: {self.get_phones()}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find_record_by_name(self, name: str) -> Record:
        res = self.data.get(name.capitalize())
        if not res:
            raise ValueError(LEVEL_ERROR + ' ' + NOT_FOUND)
        return res

    def find_record_by_phone(self, phone: str) -> Record:
        phone = Phone(phone)
        if phone is None:
            raise ValueError(LEVEL_ERROR + ' ' + GIVE_PHONE)

        found = None
        for record in self.data.values():
            if phone.value in [p.value for p in record.phones]:
                found = record

        if not found:
            raise ValueError(LEVEL_ERROR + ' ' + NOT_FOUND)

        return found

    def delete_record(self, name: str) -> None:
        record = self.data.get(name.capitalize())
        if record is None:
            raise ValueError(LEVEL_ERROR + ' ' + NOT_FOUND)

        del self.data[name.capitalize()]

    def print_all(self) -> str:
        res = ''
        for rec in self.data.values():
            res += f"{str(rec)}\n"
        return res
