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


def _iter_tree_entries(oid):
    """
    This function iterates over tree entries.
    If the oid is None, it returns None.
    Otherwise, it gets the object with the given oid and type TREE,
    decodes it, splits it into lines, and for each line,
    it splits the line into type_, oid, and name, and yields these values.
    """
    if not oid:
        return
    tree = data.get_object(oid, TREE)
    for entry in tree.decode().splitlines():
        type_, oid, name = entry.split(" ", 2)
        yield type_, oid, name


def get_tree(oid, base_path=""):
    """
    This function is used to get a tree structure.

    Parameters:
    oid (str): The object ID of the root of the tree.
    base_path (str): The base path for the tree. Default is an empty string.

    Returns:
    dict: A dictionary representing the tree structure.
    """

    result = {}  # Initialize an empty dictionary to store the result

    # Iterate over each entry in the tree
    for type_, oid, name in _iter_tree_entries(oid):
        assert "/" not in name  # Ensure that the name does not contain a slash
        assert name not in ("..", ".")  # Ensure that the name is not ".." or "."

        path = base_path + name  # Construct the path

        if type_ == BLOB:
            result[path] = oid
        elif type_ == TREE:
            result.update(get_tree(oid, f"{path}/"))
        else:
            assert False, f"Unknown tree entry {type_}"

    return result  # Return the resulting tree structure


def read_tree(tree_oid):
    """
    This function reads a tree structure and writes the data to files.

    Parameters:
    tree_oid (str): The object ID of the root of the tree.
    """

    # Get the tree structure and iterate over each item
    for path, oid in get_tree(tree_oid, base_path="./").items():
        # Create the necessary directories for the path
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Open the file at the path in write-binary mode
        with open(path, "wb") as f:
            # Write the data of the object with the given OID to the file
            f.write(data.get_object((oid)))


def is_ignored(path):
    return ".hit" in path.split("/")
