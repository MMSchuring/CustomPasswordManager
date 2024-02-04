from cryptography.fernet import Fernet
import os
import Defaults as d

# Get current directory and assign target path TODO: replace with path from setting file


class Cryptor:

    def __init__(self):
        self.key = None
        self.password_dict = {}
        dir_path = os.path.dirname(os.path.realpath(__file__))
        pivot = dir_path.rfind("CryptRepo")
        self.file_path = f"{dir_path[:pivot]}Resources\\"
        self.key_file = f"{self.file_path}{d.key_file}"
        self.password_file = f"{self.file_path}{d.pwd_file}"
        self.key_exists = os.path.isfile(f"{self.file_path}{d.key_file}")
        self.pwd_exists = os.path.isfile(f"{self.file_path}{d.pwd_file}")
        self.__get_key()
        self.__get_password_file()

    def __generate_key(self):
        key = Fernet.generate_key()
        with open(f"{self.file_path}{d.key_file}", 'wb') as f:
            f.write(key)

    def __get_key(self):
        if not self.key_exists:
            self.__generate_key()
        with open(self.file_path + d.key_file, 'rb') as f:
            self.key = f.read()

    def __get_password_file(self):
        if not self.pwd_exists:
            return

        with open(self.password_file, 'r') as f:
            for line in f:
                name, encrypted = line.split(d.separator)
                self.password_dict[name] = encrypted.rstrip()

    def save_password_file(self):
        content = ""
        for name, password in self.password_dict.items():
            content += f"{name}{d.separator}{password}\n"
        content = content.rstrip()
        with open(self.password_file, 'w+') as f:
            f.write(content)

    def add_password(self, name, password):
        """Adds a new entry to the password dict"""
        encrypted = Fernet(self.key).encrypt(password.encode()).decode()
        self.password_dict[name] = encrypted

    def get_password(self, name):
        """Returns the password for the given name"""
        return Fernet(self.key).decrypt(self.password_dict[name].encode()).decode()

    def remove_password(self, name):
        del self.password_dict[name]
