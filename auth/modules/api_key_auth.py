from __future__ import annotations
import bcrypt
import secrets


class ApiKeyAuthModule:
    """Basic API key style authentication where user must pass 
    in valid data for both "X-ACCESS and X-API-KEY headers in order 
    to successfully authenticate.
    """

    @staticmethod
    def _generate_api_key() -> str:
        return secrets.token_urlsafe(64)
    
    @classmethod
    def hash_api_key(cls, api_key:str) -> bytes:
        return bcrypt.hashpw(api_key.encode('utf-8'), bcrypt.gensalt())
    
    @classmethod
    def create_user_key(cls) -> str:
        """Returns a bcrypt-hashed-and-salted API key to store in the DB."""
        key = cls._generate_api_key()
        return cls.hash_api_key(key).decode('utf-8')

    @staticmethod
    def verify_api_key(api_key:str, hashed_api_key:str) -> bool:
        return bcrypt.checkpw(api_key.encode('utf-8'), hashed_api_key.encode('utf-8'))
    

    # def _is_ipython(self) -> bool:
    #     """Print the secret key to the terminal ONLY if we 
    #     are running in an iPython shell.
    #     """
    #     try:
    #         get_ipython
    #     except NameError:
    #         return False
    #     else:
    #         return True

