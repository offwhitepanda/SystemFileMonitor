import os
import sqlite3
import datetime
import platform
from compute_file_hashes import compute_file_hash
from import_exceptions import import_exceptions
from to_json import to_json
from utility_commands import print_colorful
from utility_commands import files_checked_progress
from send_message import send_toast_if_changes_detected


def check_file_hashes():
    print_colorful("Checking file hashes", "green")
    bool_hash_change = False
    files_excepted_by_path_count = 0
    files_excepted_by_extension_count = 0
    files_with_permission_denied = 0
    files_with_different_hashes = 0
    files_checked = 0
    entries = []

    # Import the dynamic variable exceptions arrays from the import_exceptions module
    exceptions = import_exceptions()

    # Assign the exceptions arrays to specific variables
    EXCEPTIONS_BY_PATH = exceptions.get("exceptions_by_path", [])
    EXCEPTIONS_BY_EXTENSION = exceptions.get("exceptions_by_extension", [])

    if "Ubuntu" in platform.version():
        print("System is Ubuntu")
        system32_dir = '/usr/bin'
    else:
        system32_dir = 'C:\\Windows\\System32'

    conn = sqlite3.connect('file_hashes.db')
    cursor = conn.cursor()

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
                stored_hash = cursor.execute('SELECT hash FROM file_hashes WHERE file_path = ?',
                                             (file_path,)).fetchone()

                if stored_hash:
                    file_hash = compute_file_hash(file_path)
                    stored_hash = stored_hash[0]

                    if file_hash != stored_hash:
                        files_with_different_hashes += 1

                        current_datetime = datetime.datetime.now().isoformat()

                        # Create a dictionary for the current entry
                        entry = {
                            "file_path": file_path,
                            "stored_hash": stored_hash,
                            "file_hash": file_hash,
                            "current_datetime": current_datetime
                        }

                        # Append the entry to the list
                        entries.append(entry)

                        bool_hash_change = True

            except PermissionError:
                files_with_permission_denied += 1

            files_checked += 1
            files_checked_progress(files_checked)

    conn.close()
    print()
    print(f"Files Excepted By Path: {files_excepted_by_path_count}")
    print(f"Files Excepted By Extension: {files_excepted_by_extension_count}")
    print(f"Files With Permission Denied: {files_with_permission_denied}")
    print(f"Files With Different Hashes: {files_with_different_hashes}")
    to_json(entries)

    # Send message if changes detected
    send_toast_if_changes_detected(bool_hash_change, files_with_different_hashes)

    return bool_hash_change


if __name__ == "__main__":
    check_file_hashes()