from collections import UserDict
from datetime import datetime
import re

class Field:
    def __init__(self, value) -> None:
        self.__value = None
        # self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        # if len(value) > 0:
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
    def __init__(self, value = None) -> None:
        self.__value = None
        self.value = value
    
    @Field.value.setter
    def value(self, value:str):
        if value:
            number = re.sub(r'\D', '', value)               
            if bool(re.search(r"^(38)?\d{10}$", number)) is not True:
                raise ValueError("Phone number is invalid!")
        self.__value = value
        # Field.value.fset(self, value)   

    def __str__(self) -> str:
        return self.__value
    
    def __repr__(self) -> str:
        return self.__value
    
class Birthday(Field):

    def __init__(self, value = None) -> None:
        self.__value = None
        self.value = value

    @Field.value.setter
    def value(self, value : str) -> datetime:
        if value:
            try:
                birth = datetime.strptime(value, '%d/%m/%Y').date() 
                today = datetime.now().date()
                if birth > today:
                    raise ValueError('The date is invalid! Enter real date.')
                self.__value = birth
                # Field.value.fset(self, value)                                           
            except:
                raise ValueError('The date is invalid! The date has format dd/mm/yy')
        
    def __str__(self) -> str:
        return self.__value
    
    def __repr__(self) -> str:
        return str(self.__value)


class Record:   
    
    def __init__(self, 
                 name:Name, 
                 phone: Phone | str | None =None,
                 birth: Birthday| str | None =None,) -> None:
                 
        self.phones = []
        if birth:
            self.birth = Birthday(birth)
        self.birth = birth
        self.name = name        
        if phone:
            # self.phones.append(Phone(phone))
            self.add_phone(phone)

        self.user_record = {'name': self.name,
                     'phones': self.phones,
                     'birthday': self.birth}
    

    def add_phone(self, phone: Phone | str):
        Phone(phone)
        if phone not in self.phones:
            self.phones.append(phone)
            # self.user_record.get('phones').append(phone)
        return self.phones
     
    def remove_phone(self, phone):
        self.user_record.get('phones').remove(phone)
        return self.user_record
    
    def edit_phone(self, new_phone): 
        self.add_phone(new_phone)
        return self.user_record
    
    def add_birthday(self, birth: Birthday | str):
        self.user_record['birthday'] = Birthday(birth)
        # self.user_record['birthday'] = birth
        return self.user_record
    
    def days_to_birthday(self) -> int:
        self.day_, self.month_, self.year_ = self.birth.split('/')
        self.year_ = datetime.now().date().year
        self.birthday = datetime(year=int(self.year_), month=int(self.month_), day= int(self.day_)).date()
        self.current_datetime = datetime.now().date()
        if self.birthday < self.current_datetime:
            self.birthday = datetime(year=int(self.year_) + 1, month=int(self.month_), day= int(self.day_)).date()
        self.days_amount = self.birthday - self.current_datetime
        return f"{self.days_amount.days} days until next bithday for user {self.name}"
    

    def __str__(self) -> str:        
        return '{}:   phones {},   date of birth {}'.format(self.name, self.phones, self.birth)
    
    def __repr__(self) -> str:
        return str(self)


class AddressBook(UserDict):
    # 
    def __init__(self, record: Record | None = None) -> None:
        self.data = {}
        if record is not None:
            self.add_record(record)      

   
    def add_record(self, record: Record):
        self.data[record.name] = record
        # return self.data

    
    def show_record(self, name):
            return self.data.get(name)

    def show_all(self):
        for name, record in self.data.items():            
            print(f'{name}: {record.user_record}')

    def __str__(self) -> str:
        return self.data.items()
         
    def __repr__(self) -> str:
        return str(self)
    

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
        if self.current_value < self.n and self.current_value<len(self.book):
            self.ind = self.current_value
            self.current_value += 1
            next_names = self.list_names [self.ind: self.ind + self.n] # імена records які потрібно вивести
            name = next_names[0] 
            result = self.book[name]
            return  result
            
        raise StopIteration
    

ab_dict = AddressBook()    
user1 = Record('Alina','0679255631', '13/03/1973')
# user2 = Record('Mykola')
# user3 = Record('Tutor','0676569847')
# user2.add_birthday('05/12/1995')
user1.add_phone('8888888888')
user1.add_phone('8888888888')
print(user1.user_record)
# print(user2.user_record)
# user2.add_phone('0987456323')
# print(user2.user_record)

# print(user1.user_record)
user1.remove_phone('0679255631')
# print(user1.user_record)
# ab_dict.add_record(user2)
ab_dict.add_record(user1)
user1.add_phone('8888888888')

print(user1.user_record)

# ab_dict.add_record(user3)
# print(ab_dict.show_all())
# days = user1.days_to_birthday()
# print(days)


iter = Iterable(2, ab_dict.data)
for i in iter:
    print(i)

a = Phone('380679140577')
print(a)

print(ab_dict.show_all())
print(ab_dict.show_record('Alina'))
print(ab_dict.show_record('Katya'))


# В этой домашней работе вы должны реализовать такие классы:

# Класс AddressBook, который наследуется от UserDict, и мы потом добавим логику поиска по записям в этот класс.
# Класс Record, который отвечает за логику добавления/удаления/редактирования необязательных полей и хранения обязательного поля Name.
# Класс Field, который будет родительским для всех полей, в нем потом реализуем логику общую для всех полей.
# Класс Name, обязательное поле с именем.
# Класс Phone, необязательное поле с телефоном и таких одна запись (Record) может содержать несколько.


# Критерии приёма

# Реализованы все классы из задания.
# Записи Record в AddressBook хранятся как значения в словаре. В качестве ключей используется значение Record.name.value.
# Record хранит объект Name в отдельном атрибуте.
# Record хранит список объектов Phone в отдельном атрибуте.
# Record реализует методы для добавления/удаления/редактирования объектов Phone.
# AddressBook реализует метод add_record, который добавляет Record в self.data.



    




