class StorageError(Exception):
    pass

class TitleNotFoundError(StorageError):
    pass

class BookReqFoundError(StorageError):
    pass

class InvalidEmailFormat(Exception):
    pass