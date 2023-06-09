from collections import UserDict
from datetime import datetime
import re

class Field:
    def __init__(self, value) -> None:
        self.value = value
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value
    
    def __str__(self) -> str:
        return self.__value

    def __repr__(self) -> str:
        return self.__value


class Name(Field):
    def __init__(self, value) -> None:
        # self.__value = None
        self.value = value
  
    def __repr__(self) -> str:
        return self.value


class Phone(Field):
    def __init__(self, value) -> None:
        self.value = value

    @Field.value.setter
    def value(self, value:str):
        if value:
            number = re.sub(r'\D', '', value)
            if bool(re.search(r"^(38)?\d{10}$", number)) is not True:
                raise ValueError("Phone number is invalid!")
        Field.value.fset(self, value)


class Birthday(Field):

    def __init__(self, value ) -> None:
        self.value = value

    @Field.value.setter
    def value(self, value : str) -> None:
        if value:
            try:
                value = value.strip()
                birth = datetime.strptime(value, '%d/%m/%Y').date()
                today = datetime.now().date()
                if birth > today:
                    raise ValueError('The date is invalid! Enter real date.')

                Field.value.fset(self, birth)
                
            except:
                raise ValueError('The date is invalid! The date has format dd/mm/yy')

    def __str__(self) -> str:
        if self.value is not None:
            return self.value.strftime('%d/%m/%Y')
        return 'Empty'

    def __repr__(self) -> str:
        if self.value is not None:
            # return f'Birtday({self})'
            return f'{self}'
        return 'Empty'


class Record:
    def __init__(self,
                 name:Name,
                 phone: Phone | str | None =None,
                 birth: Birthday| str | None =None,) -> None:

        self.name = name
        self.phones = []

        self.birth = None

        if birth:
            self.add_birthday(birth)

        if phone:
            self.add_phone(phone)

    @property
    def user_record(self):
        return {'name': self.name,
                    'phones': self.phones,
                    'birthday': self.birth}

    # Перевіримо наяність телефона у списку телефонів за його значенням
    # якщо є повернемо його інакше повернеться None
    def search(self, phone: Phone | str):
        if isinstance(phone, Phone):
            phone = phone.value
        for p in self.phones:
            if p.value == phone:
                return p

    def add_phone(self, phone: Phone | str):
        # Якщо телефон є ми не додамо
        if self.search(phone):
            return self.user_record
        #  Якщо телефон як строка прийшов, потрібно створити екземпляр
        if isinstance(phone, str):
            phone = Phone(phone)
        self.phones.append(phone)
        return self.user_record

    def remove_phone(self, phone):
        # Знайдемо екземпляр телефону у списку за значенням
        # видалити ми можемо саме екземпляр тому що у нас список екземплярів
        old_phone = self.search(phone)
        if old_phone:
            return self.phones.remove(old_phone)
        return self.user_record

    def edit_phone(self, old_phone, new_phone):
        phone = self.search(old_phone)
        # якщо ми передамо екземпляри
        if isinstance(new_phone, Phone):
            new_phone = Phone.value
        if phone:
            phone.value = new_phone
        return self.user_record

    def add_birthday(self, birth: Birthday | str):
        if isinstance(birth, str):
            birth = Birthday(birth)
        self.birth = birth
        return self.user_record

    def days_to_birthday(self) -> int:

        if self.birth is None:
            return -1

        current_datetime = datetime.now().date()
        birthday = self.birth.value.replace(year=current_datetime.year)
        if birthday < current_datetime:
            birthday = birthday = self.birth.value.replace(year=current_datetime.year + 1)
        days_amount = (birthday - current_datetime).days
        # return f"{days_amount} days until next bithday for user {self.name}"
        return days_amount

    def show_phones(self):
        return ' , '.join([p.value for p in self.phones])

    def __str__(self) -> str:
        return f'{self.name}: phones {self.show_phones()}, date of birth {self.birth}'



class AddressBook(UserDict):
    def __init__(self, record: Record | None = None) -> None:
        self.data = {}
        if record is not None:
            self.add_record(record)

    def add_record(self, record: Record):
        if record.name not in self.data:
            self.data[record.name] = record
    
                
    def show_record(self, name):
        return self.data.get(name)

    def show_all(self):
        for name, record in self.data.items():
            print(f'{name}: {record.user_record}')

    def __str__(self) -> str:
        return '\n'.join([str(record) for record in self.data.values()])


# ITERATOR
class Iterable:
    def __init__(self, n, records):
        self.current_value = 0
        self.n = n
        self.book = records
        self.list_names = list(records)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_value < self.n and self.current_value < len(self.book):
            self.ind = self.current_value
            self.current_value += 1
            next_names = self.list_names[self.ind: self.ind + self.n] # імена records, які потрібно вивести
            name = next_names[0]
            result = self.book[name]
            return f'{self.current_value}: {result}'

        raise StopIteration


ab_dict = AddressBook()
user1 = Record('Alina', '0679255631', '13/03/1973')
user2 = Record('Mykola')
user3 = Record('Tutor','0676569847')
user2.add_birthday('05/12/1995')
user1.add_phone('8888888888')
user1.add_phone('8888888888')
print(user1.user_record)
print(user2.user_record)
user2.add_phone('0987456323')
print(user2.user_record)

print(user1.user_record)
user1.remove_phone('0679255631')
print(user1.user_record)
ab_dict.add_record(user2)
ab_dict.add_record(user1)
user1.add_phone('8888888888')

print(user1.user_record)

ab_dict.add_record(user3)
print(ab_dict.show_all())
days = user1.days_to_birthday()
print(f'******{days}')

print(ab_dict.show_all())

iter = Iterable(2, ab_dict.data)
for i in iter:
    print(i)

# print(ab_dict.show_all())
# print(ab_dict.show_record('Alina'))
# print(ab_dict.show_record('Katya'))




    




