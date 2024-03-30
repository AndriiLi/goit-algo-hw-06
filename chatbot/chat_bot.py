from colorama import Fore

from chatbot.classes import AddressBook, Record
from chatbot.command_parser import parse_input
from chatbot.command_handlers import add_contact, change_phone, all_contacts, export_contacts, \
    import_contacts, delete_contact, find_contact_by_name, find_contact_by_phone, add_phone, del_phone
from chatbot.constants import LEVEL_ERROR, LEVEL_WARNING, MESSAGE_LEVELS, INVALID_COMMAND


def print_colored(message: str | Exception) -> None:
    message = str(message) if isinstance(message, Exception) else message
    color = Fore.BLUE
    if message.startswith(LEVEL_ERROR):
        color = Fore.RED

    if message.startswith(LEVEL_WARNING):
        color = Fore.YELLOW

    for marker in MESSAGE_LEVELS:
        message = message.replace(marker, '').strip()

    print(f"{color}{message}{Fore.RESET}")


def run_chat_bot() -> None:
    address_book = AddressBook()

    print_colored("Welcome to the assistant bot!")

    while True:
        try:
            user_input = input("Enter a command: ")

            command, *args = parse_input(user_input)
            match command:
                case "close" | "exit" | "q" | "quit":
                    print_colored("Good bye!")
                    break
                case "hello" | "hi":
                    print_colored("How can I help you?")
                case "add":
                    print_colored(add_contact(args=args, address_book=address_book))
                case "contact":
                    print_colored(find_contact_by_name(args=args, address_book=address_book))
                case "phone":
                    print_colored(find_contact_by_phone(args=args, address_book=address_book))
                case "del":
                    print_colored(delete_contact(args=args, address_book=address_book))
                case "change":
                    print_colored(change_phone(args=args, address_book=address_book))
                case "addphone":
                    print_colored(add_phone(args=args, address_book=address_book))
                case "delphone":
                    print_colored(del_phone(args=args, address_book=address_book))
                case "all":
                    print_colored(all_contacts(address_book=address_book))
                case "save":
                    print_colored(export_contacts(address_book=address_book))
                case "load":
                    print_colored(import_contacts(address_book=address_book))
                case _:
                    raise ValueError(LEVEL_ERROR + " " + INVALID_COMMAND)

        except Exception as e:
            print_colored(e)
