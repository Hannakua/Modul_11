import sys
from classes_2 import AddressBook, Record, Phone, Birthday, Iterable

USERS = AddressBook()
  
def error_handler(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except KeyError:
            return "No such user."
        except ValueError:
            return 'Please, give me the name and phone number(38XXX-XXX-XX or XXX-XXX-XX-XX) or birth in format dd/mm/yyyy.'
        except IndexError:
            return 'Enter user name.'
        except TypeError:
            return "Example: add Tomas, 0506936985"
    return inner


def hello():
    name = input('Hello, I am Bot. What is your name? ')
    return f'Hello, {name}! Can I help you?'

@error_handler
def unknown_command():
    
    return f"The command is wrong or empty. Please write command again or write help to see the possible command list."


def help():
    return "I am a bot. I accept the following commands: 'hello', 'add', 'change', 'show all', 'print' 'exit', 'goodbye', 'close', 'birth'. For 'add' or 'change' commands please enter the command in sequence: command user_name comma backspace user_number. For example: 'add Taras Kovalenko, 0676542345'"

@error_handler
# def add_user(name, phone, birth):
def add_user(name, phone):
    
    user = Record(name, phone)

    # user = Record(name, phone, birth)
    user.add_phone(phone)    
    USERS.add_record(user)

    # record = Record(name, phone)
    # record.add_phone(phone)
    # result = USERS.add_record(record)
  
    result = user.user_record
    return result

# @error_handlers
def add_birth(name, birth):
    user = USERS[name]
    user.user_record.add_birthday(birth)
    return user.user_record


@error_handler
def change_phone(name, new_num):
    
    if name in USERS.keys():        
        USERS.pop(name)      
    record = Record(name, new_num)
    record.edit_phone(new_num)
    result = USERS.add_record(record) 
    # old_num=USERS[name]
    
    return f'New phone number {new_num} is saved for {name}. Old numbers were deleted. \n{result}'

@error_handler
def phone_show(name):
    # name = ''.join(name)
    number = USERS.get(name, f'user is not in phone book yet')
    return f'Phone number for user {name} is: {number}.'


def show_all():
    # result = '\n'
    if USERS == {}:
        result = "Not any record in phone book yet."
    else:
        USERS.show_all()

def show_part(n):
    iter = Iterable(int(n), USERS.data)
    for i in iter:
        print(i)

    

def exit():
    print('Good Bye!') 
    return sys.exit()

HANDLERS = {
    'help': help,
    'add': add_user,
    'show all': show_all,
    'exit': exit,
    'phone show': phone_show,
    'close': exit,
    'good bye': exit,
    'change': change_phone,  
    'birth': add_birth, 
    'print': show_part,
}


def identeficate_command(user_input):

    user_command, *data = user_input.strip().split(' ', 1)

    try:
        handler = HANDLERS[user_command.lower()]
        
    except KeyError:
        if data:
            command_part2, *data = data[0].strip().split(' ', 1)
            user_command = user_command + ' ' + command_part2       # якщо команда складається з двох слів через пробіл
        handler = HANDLERS.get(user_command.lower(), unknown_command)

    if data:
        data = data[0].split(',')
    print(data)
        
    return handler, data


def main():

    print(hello())

    while True:
        user_input = input('Please enter command: ')
    
        handler, data= identeficate_command(user_input)
   
        result = handler(*data)

        print(result)


if __name__ == "__main__":
    main()