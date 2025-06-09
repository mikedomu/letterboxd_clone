# password_hasher.py

"""
Module responsible for secure password hashing and verification.
"""

import bcrypt

class PasswordHasher:
    """
    Static class for hashing and verifying user passwords.
    Uses bcrypt algorithm.
    """

    @staticmethod
    def hash(password: str) -> str:
        """
        Hashes user password using bcrypt.

        :param password: Password to hash.
        :type password: str
        :return: Hashed password.
        :rtype: str
        """
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash_bytes = bcrypt.hashpw(password_bytes, salt)
        return password_hash_bytes.decode('utf-8')

    @staticmethod
    def verify(password_input: str, password_from_users_data: str) -> bool:
        """
        Verifies if provided password matches the hashed password.

        :param password_input: Input password.
        :type password_input: str
        :param password_from_users_data: Hashed password from database.
        :type password_from_users_data: str
        :return: True if passwords match, False otherwise.
        :rtype: bool
        """
        return bcrypt.checkpw(password_input.encode('utf-8'), password_from_users_data.encode('utf-8'))
