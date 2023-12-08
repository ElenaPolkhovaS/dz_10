"""
Модуль для управління адресною книгою
"""
from collections import UserDict

class Field:
    """Базовий клас для полів запису"""
    def __init__(self, value):
        self.value = value

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

class Record:
    """Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів"""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

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

    def __str__(self):
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
