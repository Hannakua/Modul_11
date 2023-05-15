from collections import UserDict
from datetime import datetime, timedelta
import re

class Field:
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value


    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) > 0:
            self.__value = value

    def __str__(self) -> str:
        return f"{self.__value}"


class Name(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        
    def __repr__(self) -> str:
        return self.__value


class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(value)


    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value:str):
        number = re.sub(r'\D', '', value)
        if bool(re.search(r"^(38)?\d{10}$", number)) == True:
            self.__value = value
                       
        else:
            raise ValueError("Phone number is invalid!")
      
    def __repr__(self) -> str:
        return self.__value
    
class Birthday(Field):

    def __init__(self, value) -> None:
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value : str) -> datetime:
        try:
            birth = datetime.strptime(value, '%d/%m/%Y').date() 
            today = datetime.now().date()
            if birth < today:
                self.__value = birth
            else:
                 print("This date has not yet arrived :-) Please input a real date  of birth.")                                
        except:
            raise ValueError('The date is invalid!')
        
    def __repr__(self) -> str:
        return self.__value


class Record:   
    
    def __init__(self, 
                 name: Name, 
                 phone: Phone | str | None =None,
                 birth: Birthday| str | None =None,) -> None:
        self.phones = set()
        self.birth = None
        self.name = name        
        if phone:
             self.phones.add(phone)
        if birth:
            self.birth = birth
        # self.user_record = {self.name: self.phones}
        self.user_record = {'name': self.name,
                     'phones': self.phones,
                     'birthday': self.birth}
    

    def add_phone(self, phone):
        # self.user_record.get(self.name).add(phone)
        self.user_record.get('phones').add(phone)
        return self.user_record
    
    def remove_phone(self, phone):
        self.user_record.get('phones').discard(phone)
        return self.user_record
    
    def edit_phone(self,  new_phone):   #old_phone,
        # self.remove_phone(old_phone)
        self.add_phone(new_phone)
        return self.user_record
    
    def days_to_birthday(self) -> int:
        # input_date = input('Birthday input: ')
        self.day_, self.month_, self.year_ = self.birth.split('/')
        self.year_ = datetime.now().date().year
        self.birthday = datetime(year=int(self.year_), month=int(self.month_), day= int(self.day_)).date()
        self.current_datetime = datetime.now().date()
        if self.birthday<self.current_datetime:
            self.birthday = datetime(year=int(self.year_)+1, month=int(self.month_), day= int(self.day_)).date()
        self.days_amount = self.birthday - self.current_datetime
        return f"{self.days_amount.days} days until next bithday for user {self.name}"
    

    def __str__(self) -> str:        
        return self.user_record.items()
    
    # def __repr__(self) -> str:
    #     return str(self)


class AddressBook:
    # 
    def __init__(self, record: Record | None = None) -> None:
        self.records = {}
        if record is not None:
            self.add_record(record)      

   
    def add_record(self, record: Record):
        self.records[record.name] = record
        return self.records

    
    def show_all(self):
        for inx, record in enumerate(self.records.values()):
            print(f'{inx}: {record.user_record}')

    # def show(self):
    #     for name, record in self.records.items():            
    #         print(f'{name}: {record.user_record}')
            

    def __str__(self) -> str:
        return self
    
    def __repr__(self) -> str:
        # return f"Name(value={self.value})"
        return self.records
    

# ITERATOR
class Iterable:
    # amount = len(AddressBook().records)
    book = AddressBook().records
    def __init__(self, n):              # n -по скільки записів виводити на сторінку
        self.current_value = 0
        self.n = n             
        
    def __next__(self):
        if self.current_value < self.n: # and self.current_value<self.amount:
            self.ind = self.current_value
            self.current_value += 1
            
            # return f"{self.current_value}: {list(self.book.values())[self.ind]}"

            return f"{self.current_value}: ..."
            
        raise StopIteration


class CustomIterator:
    def __init__(self, n):
        self.n = n

    def __iter__(self):        
        return Iterable(self.n)

    
ab_dict = AddressBook()    
user1 = Record('Alina','06792563', '13/03/1973')
user2 = Record('Mykola')
user3 = Record('Tutor','0676569847')
print(user1.user_record)
print(user2.user_record)
user2.add_phone('9874563223')
print(user2.user_record)
user1.add_phone('888888888')
print(user1.user_record)
user1.remove_phone('06792563')
print(user1.user_record)
ab_dict.add_record(user2)
ab_dict.add_record(user1)
ab_dict.add_record(user3)
print(ab_dict.show_all())
days = user1.days_to_birthday()
print(days)

c = CustomIterator(2)
for i in c:
    print(i)

print(ab_dict.records.values())
 

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



    




