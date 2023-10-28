# goitneo-python-hw-3-Group3
Installation and Usage Guide for Homework_modul12_3.1 final version.py
Introduction:
The provided script Homework_modul12_3.1 final version.py is a comprehensive address book management system that allows users to add, modify, and search for contacts. It supports functionalities such as adding and changing phone numbers and birthdays, searching contacts by name or phone number, and showing upcoming birthdays in a week.

Prerequisites:
Python 3.6 or newer
A terminal or command-line interface
Installation:
Save the given script as Homework_modul12_3.1 final version.py in your desired directory.
Navigate to the directory containing the script using your terminal or command-line interface.
Usage:
Running the Program:
In the terminal, run the following command to start the address book program:
Copy code
python Homework_modul12_3.1 final version.py
Available Commands:
hello: Greet the program.
add: Add a contact.
Format: add <name> <phone>
change: Change a contact's phone number.
Format: change <name> <old_phone> <new_phone>
find: Find a contact by name or phone.
Format: find <name_or_phone>
delete: Delete a contact by name.
Format: delete <name>
all: Show all contacts.
save: Save the address book to a file (addressbook.pkl by default).
load: Load the address book from a file (addressbook.pkl by default).
add-birthday: Add or change a contact's birthday.
Format: add-birthday <name> <DD.MM.YYYY>
show-birthday: Show a contact's birthday.
Format: show-birthday <name>
birthdays: Show upcoming birthdays for the week, shifting all birthdays that happened in preceding weekend to Monday.
help: Display available commands and their descriptions.
close or exit: Exit the program.
Additional Notes:
For commands like add, change, and add-birthday, make sure to provide all required arguments.
When saving or loading the address book, it uses a file named addressbook.pkl by default. Make sure not to delete this file if you want to retain your saved contacts.
Always remember to save your changes before closing the program if you want to keep them.
Enjoy managing your contacts with this tool!
