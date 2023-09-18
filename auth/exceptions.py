

class AuthException(BaseException):
    """Base class for authenitcation exceptions"""
    pass

class AuthModuleNotFound(AuthException):
    """Raised when an auth module's authenticate() method has not 
    properly subclassed the AuthModuleBase's authenticate() method.
    """
    pass

class PermissionDenied(AuthException):
    """Raised when user has authenticated succcessfuly,
    but does not hold required permissions to access resource.
    """
    pass

class ApiKeyException(AuthException):
    """Base class for API key exceptions"""
    pass

class HmacException(AuthException):
    """Base class for HMAC exceptons"""
    pass


# API Key Exceptions
# ========================================================
class UserInvalid(ApiKeyException):
    """Raised when the submitted UUID can not be found in 
    the User table
    """
    pass

class UserValidKeyInvalid(ApiKeyException):
    """Raisd when both user and key headers are present, 
    but user's acces_id is valid and key is invalid
    """
    pass


# HMAC Exceptions
# ========================================================
