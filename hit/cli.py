import os
import sys
import argparse

from . import data


def main():
    args = parse_args()
    args.func(args)


def parse_args():
    parser = argparse.ArgumentParser()

    commands = parser.add_subparsers(dest="command")
    commands.required = True

    init_parser = commands.add_parser("init")
    init_parser.set_defaults(func=init)

    hash_object_parser = commands.add_parser("hash-object")
    hash_object_parser.set_defaults(func=hash_object)
    hash_object_parser.add_argument("file")

    cat_file_parser = commands.add_parser("cat-file")
    cat_file_parser.set_defaults(func=cat_file)
    cat_file_parser.add_argument("object")

    return parser.parse_args()


def init(args):
    """
    This function initializes an empty hit repository in the current working directory.

    Args:
        args (argparse.Namespace): The command line arguments passed to the function.
    """
    data.init()
    print(f"Initialized empty hit repository in {os.getcwd()}/{data.GIT_DIR}")


def hash_object(args):
    """
    This function reads a file, hashes its content using SHA1, and then prints the hashed data.

    Args:
        args (argparse.Namespace): The command line arguments passed to the function.
                                   'args.file' is expected to be the path to the file to be hashed.
    """
    with open(args.file, "rb") as f:
        print(data.hash_object(f.read()))


def cat_file(args):
    """
    This function retrieves an object from the hit repository and writes it to stdout.

    Args:
        args (argparse.Namespace): The command line arguments passed to the function.
                                   'args.object' is expected to be the object id of the object to be retrieved.
    """
    sys.stdout.flush()
    sys.stdout.buffer.write(data.get_object(args.object))
