import os
from . import data
from .constants import CWD, BLOB, TREE


def write_tree(directory=CWD):
    """
    This function recursively writes files in a directory (and its subdirectories) to the object store.

    Args:
        directory (str, optional): The directory to start from. Defaults to the current directory.
    """

    # Initialize an empty list for entries
    entries = []

    with os.scandir(directory) as it:
        for entry in it:
            full = f"{directory}/{entry.name}"

            # If the file or directory is ignored, we skip it
            if is_ignored(full):
                continue

            # If the entry is a file, we hash it and add it to our entries list
            if entry.is_file(follow_symlinks=False):
                type_ = BLOB
                with open(full, "rb") as f:
                    oid = data.hash_object(f.read())

            # If the entry is a directory, we recursively call this function on that directory
            elif entry.is_dir(follow_symlinks=False):
                type_ = TREE
                oid = write_tree(full)

            # Add the entry to our entries list
            entries.append((entry.name, oid, type_))

    # Create a tree object and return its hash
    tree = "".join(f"{type_} {oid} {name}\n" for name, oid, type_ in sorted(entries))

    return data.hash_object(tree.encode(), TREE)


def is_ignored(path):
    return ".hit" in path.split("/")
