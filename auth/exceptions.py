

class AuthException(BaseException):
    """Base class for authenitcation exceptions"""
    pass

class ApiKeyException(AuthException):
    """Base class for API key exceptions"""
    pass

class HmacException(AuthException):
    """Base class for HMAC exceptons"""
    pass


# API Key Exceptions
# ========================================================
class UserInvalidKeyInvalid(ApiKeyException):
    """Raised when both user and key headers are present,
    but invalid
    """
    pass

class UserValidKeyInvalid(ApiKeyException):
    """Raisd when both user and key headers are present, 
    but user's acces_id is valid and key is invalid
    """
    pass


# HMAC Exceptions
# ========================================================
