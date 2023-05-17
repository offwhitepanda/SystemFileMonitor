# This page is TODO

import json
import argparse


def remove_old_objects(file_path, max_size):

    """Removes old objects from a JSON file log once the limit is reached.

    Args:
    file_path: The path to the JSON file log.
    max_size: The maximum size of the file in bytes.

    Returns:
    The number of objects that were removed.
    """

    with open(file_path, "r") as f:
        data = json.load(f)

    num_objects_removed = 0
    while len(data) > max_size:
        data.pop(0)
        num_objects_removed += 1

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    return num_objects_removed


if __name__ == "__main__":

    # Create an ArgumentParser object.
    parser = argparse.ArgumentParser()

    # Add an argument for the max size.
    parser.add_argument("-max_size", type=int, default=10000)

    # Parse the command-line arguments.
    args = parser.parse_args()

    # Get the max size from the arguments.
    max_size_1 = args.max_size

    file_path_1 = "file_info.json"

    num_objects_removed_1 = remove_old_objects(file_path_1, max_size_1)

    print(f"{num_objects_removed_1} objects were removed.")
