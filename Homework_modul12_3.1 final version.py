import re
from collections import UserDict, defaultdict
from datetime import datetime, timedelta
import pickle


# Field Class
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Name Class
class Name(Field):
    pass

# Phone Class
class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError(f"{Colors.RED}Phone number must contain exactly 10 digits.{Colors.END}")
        self.value = value

    @staticmethod
    def validate(phone):
        return bool(re.fullmatch(r'\d{10}', phone))

# Birthday Class
class Birthday(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError(f"{Colors.RED}Birthday must be in the format DD.MM.YYYY.{Colors.END}")
        self.value = datetime.strptime(value, '%d.%m.%Y').date()

    @staticmethod
    def validate(birthday):
        try:
            datetime.strptime(birthday, '%d.%m.%Y')
            return True
        except ValueError:
            return False

# Record Class
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[idx] = Phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        birthday_str = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_str}"
    
    
    def edit_birthday(self, birthday):
        self.birthday = Birthday(birthday)

# AddressBook Class

class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def all_records(self):
        return list(self.data.values())

    def find_by_phone(self, phone):
        for record in self.data.values():
            if any(p.value == phone for p in record.phones):
                return record
        return None
        
    def get_birthdays_for_week(self):
        today = datetime.today().date()
        start_of_week = today - timedelta(days=(today.weekday() - 5) % 7)  # Shift to Saturday
        birthdays_by_day = defaultdict(list)

        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                
                # Check if the birthday is on Saturday or Sunday, shift it to Monday
                if birthday_this_year == start_of_week or birthday_this_year == start_of_week + timedelta(days=1):
                    birthdays_by_day["Monday"].append(record.name.value)

                # Check if the birthday is from Monday to Friday of the current week
                elif start_of_week + timedelta(days=2) <= birthday_this_year <= start_of_week + timedelta(days=6):
                    day_name = (birthday_this_year - start_of_week).days - 2  # Shift by 2 days to align with start being Saturday
                    day_string = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"][day_name]
                    birthdays_by_day[day_string].append(record.name.value)

        return birthdays_by_day
        return instance
     
    def save_to_file(self, filename="addressbook.pkl"):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    @classmethod
    def load_from_file(cls, filename="addressbook.pkl"):
        instance = cls()
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                instance.data = pickle.load(file)

        return instance

# Colors class
class Colors:
    GREEN = '\033[92m'   # Green
    YELLOW = '\033[93m'  # Yellow
    RED = '\033[91m'     # Red
    CYAN = '\033[96m'    # Cyan
    END = '\033[0m'      # Reset Color

    

# Bot functions
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"{Colors.RED}{str(e)}{Colors.END}"
        except KeyError:
            return f"{Colors.YELLOW}Contact not found.{Colors.END}"
        except IndexError:
            return f"{Colors.YELLOW}Incomplete command. Please check and try again.{Colors.END}"
    return inner

def parse_input(user_input):
    return user_input.split()

@input_error
def add_contact(args, book):
    if len(args) < 2:
        return "You need to provide both a name and a phone number to add a contact."
    name, phone = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return "Contact added."

@input_error
def change_contact(args, book):
    if len(args) != 3:
        return "Please provide a name, old phone, and new phone for changing contact details."
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error
def delete_contact(args, book):
    name = args[0]
    book.delete(name)
    return f"Deleted record for {name}."

@input_error
def find_by_name_or_phone(args, book):
    query = args[0]
    # Try to find by name first
    record = book.find(query)
    if not record:
        # If not found by name, try by phone
        record = book.find_by_phone(query)
    if not record:
        return "Contact not found."
    return str(record)

@input_error
def show_all(book):
    records = book.all_records()
    if not records:
        return "No contacts found."
    return "\n".join(str(record) for record in records)

@input_error

def add_birthday(args, book):
    if len(args) != 2:
        return "Please provide a name and a birthday."
    name, birthday = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    
    if record.birthday:
        response = input(f"{name} already has a birthday on {record.birthday.value.strftime('%d.%m.%Y')}. Would you like to change it? (yes/no): ")
        if response.lower() != 'yes':
            return "Birthday was not changed."
        record.edit_birthday(birthday)
        return f"{name}'s birthday updated to {birthday}."
    
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    if not record.birthday:
        return "No birthday set for this contact."
    return f"{record.name.value}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}."

@input_error
def upcoming_birthdays(book):
    birthdays = book.get_birthdays_for_week()
    if not birthdays:
        return "No birthdays in the upcoming week."
    else:
        result = []
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for day in days_order:
            if day in birthdays:
                result.append(f"{day}: {', '.join(birthdays[day])}")
        return "\n".join(result)

commands_help = {
    "hello": "Greet the program.",
    "add": "Add a contact. Format: add <name> <phone>",
    "change": "Change a contact's phone number. Format: change <name> <old_phone> <new_phone>",
    "find": "Find a contact by name or phone. Format: find <name_or_phone>",
    "delete": "Delete a contact by name. Format: delete <name>",
    "all": "Show all contacts.",
    "save": "Save the address book to a file.",
    "load": "Load the address book from a file.",
    "add-birthday": "Add or change a contact's birthday. Format: add-birthday <name> <DD.MM.YYYY>",
    "show-birthday": "Show a contact's birthday. Format: show-birthday <name>",
    "birthdays": "Show upcoming birthdays for the week.",
    "help": "Display available commands and their descriptions.",
    "close": "Exit the program.",
    "exit": "Exit the program."
  }  
    
def display_help():
    print("Available commands:")
    for command, description in commands_help.items():
        print(f"{command}: {description}") 
    
    
    
# Main execution function
import os

def main():
    # Instead of initializing a new AddressBook, load it from file
    book = AddressBook.load_from_file()
  
    while True:
        user_input = input(f"{Colors.CYAN}Enter a command:{Colors.END} ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "find":
            print(find_by_name_or_phone(args, book))
        elif command == "delete":
            print(delete_contact(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "save":
            book.save_to_file()
            print(f"{Colors.GREEN}Address book saved successfully!{Colors.END}")
        elif command == "load":
            book = AddressBook.load_from_file()
            print(f"{Colors.GREEN}Address book loaded successfully!{Colors.END}")
    # New commands
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(upcoming_birthdays(book))
        elif command == "help":
            display_help()
        else:
            print(f"'{command}' is an unrecognized command. Please provide a valid command.")

if __name__ == "__main__":
    main()