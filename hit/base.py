import os


def write_tree(directory="."):
    """
    This function recursively writes files in a directory (and its subdirectories) to the object store.

    Args:
        directory (str, optional): The directory to start from. Defaults to the current directory.
    """
    with os.scandir(directory) as it:
        for entry in it:
            full = f"{directory}/{entry.name}"
            if entry.is_file(follow_symlinks=False):
                """
                If the entry is a file, we need to write it to the object store.
                This part is not implemented yet.
                """
                print(full)
            elif entry.is_dir(follow_symlinks=False):
                # If the entry is a directory, we recursively call this function on that directory.
                write_tree(full)

    """
    After all files and directories within the current directory have been processed,
    we need to create the tree object.
    This part is not implemented yet.
    """
