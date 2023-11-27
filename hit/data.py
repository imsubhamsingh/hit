import os
import hashlib


GIT_DIR = ".hit"
BLOB = "blob"


def init():
    """
    This function is used to initialize a new Git repository.
    It creates a new directory named 'objects' inside the GIT_DIR.
    If the directory already exists, it does not throw any error
    due to the use of 'exist_ok=True'.
    """
    os.makedirs(f"{GIT_DIR}/objects", exist_ok=True)


def hash_object(data, type_=BLOB):
    """
    This function takes in data as an argument, hashes it using SHA1,
    and then writes the hashed data into a file. The file is stored
    in the 'objects' directory of GIT_DIR. The function finally
    returns the object id (oid) of the hashed data.

    Args:
        data (bytes): The data to be hashed and written into a file.
        type_ (str, optional): The type of the object. Defaults to BLOB.

    Returns:
        str: The object id (oid) of the hashed data.
    """
    obj = type_.encode() + b"\x00" + data
    oid = hashlib.sha1(obj).hexdigest()
    with open(f"{GIT_DIR}/objects/{oid}", "wb") as out:
        out.write(obj)

    return oid


def get_object(oid, expected=BLOB):
    """
    This function opens a file in binary mode for reading.
    The file is located in the 'objects' directory inside GIT_DIR and its name is the object id (oid).

    Args:
        oid (str): The object id of the file to be read.
        expected (str, optional): The expected type of the object. Defaults to BLOB.

    Returns:
        bytes: The content of the file as bytes.
    """
    with open(f"{GIT_DIR}/objects/{oid}", "rb") as f:
        obj = f.read()
    type_, _, content = obj.partition(b"\x00")
    type_ = type_.decode()

    if expected is not None:
        assert type_ == expected, f"Expected {expected}, got {type_}"

    return content
