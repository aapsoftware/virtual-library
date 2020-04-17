class StorageError(Exception):
    pass

class TitleNotFoundError(StorageError):
    pass

class BookReqFoundError(StorageError):
    pass
