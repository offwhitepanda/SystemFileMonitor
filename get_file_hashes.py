import os
import platform
from import_exceptions import import_exceptions
from compute_file_hashes import compute_file_hash
from utility_commands import files_checked_progress


def get_file_hashes():

    files_excepted_by_path_count = 0
    files_excepted_by_extension_count = 0
    files_with_permission_denied = 0
    files_checked = 0

    if "Ubuntu" in platform.version():
        print("System is Ubuntu")
        system32_dir = '/usr/bin'
    else:
        system32_dir = 'C:\\Windows\\System32'
    file_hashes = {}

    # Import the dynamic variable exceptions arrays from the import_exceptions module
    exceptions = import_exceptions()

    # Assign the exceptions arrays to specific variables
    EXCEPTIONS_BY_PATH = exceptions.get("exceptions_by_path", [])
    EXCEPTIONS_BY_EXTENSION = exceptions.get("exceptions_by_extension", [])

    for root, _, files in os.walk(system32_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            if any(file_name.startswith(exclude_file[:-5]) and file_name.endswith(exclude_file[-4:])
                   for exclude_file in EXCEPTIONS_BY_PATH):
                continue
            if file_path in EXCEPTIONS_BY_PATH:
                files_excepted_by_path_count += 1
                continue
            if any(file_path.endswith(extension) for extension in EXCEPTIONS_BY_EXTENSION):
                files_excepted_by_extension_count += 1
                continue

            try:
                file_hashes[file_path] = compute_file_hash(file_path)
            except PermissionError:
                files_with_permission_denied += 1

            files_checked += 1
            files_checked_progress(files_checked)

    print()
    print(f"Files Excepted By Path: {files_excepted_by_path_count}")
    print(f"Files Excepted By Extension: {files_excepted_by_extension_count}")
    print(f"Files With Permission Denied: {files_with_permission_denied}")
    return file_hashes
