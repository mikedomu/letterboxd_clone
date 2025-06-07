# password_hasher.py

import bcrypt

class PasswordHasher:
    """
    Klasa do hashowania i weryfikacji haseł.
    """

    @staticmethod
    def hash(password: str) -> str:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash_bytes = bcrypt.hashpw(password_bytes, salt)
        return password_hash_bytes.decode('utf-8')

    @staticmethod
    def verify(password_input: str, password_from_users_data: str) -> bool:
        return bcrypt.checkpw(password_input.encode('utf-8'), password_from_users_data.encode('utf-8'))
