"""
Модуль для управління адресною книгою
"""
from collections import UserDict
from datetime import datetime
import pickle

class Field:
    """Базовий клас для полів запису"""
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self.value)

class Name(Field):
    """Клас для зберігання імені контакту"""
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value


class Phone(Field):
    """Клас для зберігання номера телефону"""
    def __init__(self, value):
        self.validate_phone_format(value)
        super().__init__(value)

    def validate_phone_format(self, value):
        """Метод проводить валідацію номера - 10 цифр"""
        if value and not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number should be a 10-digit number")

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value


class Birthday(Field):
    """Клас для зберігання дня народження"""
    def __init__(self, value=None):
        self.validate_birthday_format(value)
        super().__init__(value)

    def validate_birthday_format(self, value):
        """Метод проводить валідацію дати"""
        try:
            return datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Birthday is not a date")

class Record:
    """Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів"""
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone_number):
        """Метод для додавання об'єктів"""
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        """Метод для видалення об'єктів"""
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break

    def find_phone(self, phone_number):
        """Метод для пошуку об'єктів"""
        for phone in self.phones:
            if phone == Phone(phone_number):
                return phone
        return None

    def edit_phone(self, old_phone_number, new_phone_number):
        """Метод для редагування об'єктів"""
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number
                return

        raise ValueError("Phone number to be edited was not found")

    def days_to_birthday(self):
        """Метод для обчислення кількості днів до наступного дня народження"""
        if isinstance(self.birthday, Birthday):
            today = datetime.now()
            today_birthday = datetime(today.year, today.month, today.day)
            day = int(self.birthday.value.strftime("%d"))
            month = int(self.birthday.value.strftime("%m"))
            year = int(today.year)
            next_birthday = datetime(year, month, day)
            if next_birthday < today_birthday:
                year = int(today.year + 1)
                next_birthday = datetime(year, month, day)
            days_left = (next_birthday - today_birthday).days
            return days_left
        return NotImplemented

    def __str__(self):
        """Метод створює рядок"""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    """Клас для зберігання та управління записами"""
    def add_record(self, record):
        """Метод додає запис до self.data"""
        record_name = record.name.value
        self.data[record_name] = record

    def find(self, name):
        """Метод знаходить запис за ім'ям"""
        if name in self.data:
            return self.data[name]
        return None

    def delete(self, name):
        """Метод видаляє запис за ім'ям"""
        if name in self.data:
            del self.data[name]

    def iterate(self, records_per_iteration=5):
        """Метод повертає генератор за записами і за одну ітерацію повертає декілька записів"""
        keys = list(self.data.keys())
        records = 0
        all_records = len(keys)
        while records < all_records:
            yield [self.data[keys[i]] for i in range(records, min(records + records_per_iteration, all_records))]
            records += records_per_iteration

    def write_to_file(self, filename):
        """Метод зберігає адресну книгу у файл"""
        with open(filename, "wb") as fh:
            pickle.dump(contacts, fh)        


    @classmethod
    def read_contacts_from_file(cls, filename):
        """Метод відновлює адресну книгу з файлу"""
        with open(filename, 'rb') as file:
            data = pickle.load(file)
            address_book = cls()
            address_book.data = data
            return address_book


    def __getstate__(self):
        """Метод контролю серіалізації"""
        state = self.__dict__.copy()
        return state


    def __setstate__(self, state):
        """Метод контролю десеріалізації"""
        self.__dict__.update(state)


    def search_records(self, query):
        """Метод проводить пошук записів за частковим збігом імені або номера телефону"""
        found_records = []
        for record in self.data.values():
            if query in record.name.value or any(query in phone.value for phone in record.phones):
                found_records.append(record)
        return found_records