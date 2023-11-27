import os
import hashlib


GIT_DIR = ".hit"


def init():
    """
    This function is used to initialize a new Git repository.
    It creates a new directory named 'objects' inside the GIT_DIR.
    If the directory already exists, it does not throw any error
    due to the use of 'exist_ok=True'.
    """
    os.makedirs(f"{GIT_DIR}/objects", exist_ok=True)


def hash_object(data):
    """
    This function takes in data as an argument, hashes it using SHA1,
    and then writes the hashed data into a file. The file is stored
    in the objects directory of the GIT_DIR. The function finally
    returns the object id (oid) of the hashed data.
    """
    oid = hashlib.sha1(data).hexdigest()
    with open(f"{GIT_DIR}/objects/{oid}", "wb") as out:
        out.write(data)

    return oid
