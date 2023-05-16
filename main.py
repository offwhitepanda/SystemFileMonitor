import hashlib
import os
import sqlite3
from win10toast import ToastNotifier
from plyer import notification

EXCEPTIONS = [
    r'perf*.dat',
    r'C:\Windows\System32\LogFiles\WMI\NetCore.etl',
    r'C:\Windows\System32\LogFiles\WMI\Wifi.etl',
    r'C:\Windows\System32\sru\SRU.chk',

]

EXCEPTIONS_BY_EXTENSION = [
    '.evtx'
]

image_path="warning.png"
bool_hash_change = False

def show_notification(message, image_path):
    notification.notify(
        title="Warning",
        message=message,
        timeout=10,
        toast=True,
        app_name="My App",
        # Specify the path to your image file
        app_icon=None
    )
def compute_file_hash(file_path):
    hasher = hashlib.sha256()

    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hasher.update(chunk)

    return hasher.hexdigest()

def get_windows_file_hashes():
    system32_dir = 'C:\\Windows\\System32'
    file_hashes = {}

    for root, _, files in os.walk(system32_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            if any(file_name.startswith(exclude_file[:-5]) and file_name.endswith(exclude_file[-4:])
                   for exclude_file in EXCEPTIONS):
                continue
            if file_path in EXCEPTIONS:
                print("Excepting by file path: " + file_path)
                continue
            if any(file_path.endswith(extension) for extension in EXCEPTIONS_BY_EXTENSION):
                print("Excepting by extension: " + file_path)
                continue

            try:
                file_hashes[file_path] = compute_file_hash(file_path)
            except PermissionError:
                print(f"Permission denied: {file_path}")

    return file_hashes


# Usage example
file_hashes = get_windows_file_hashes()

# for file_path, file_hash in file_hashes.items():
#     print(f"{file_path}: {file_hash}")

def create_database():
    conn = sqlite3.connect('file_hashes.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS file_hashes
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, file_path TEXT UNIQUE, hash TEXT)''')

    conn.commit()
    conn.close()

def insert_file_hashes(file_hashes):
    conn = sqlite3.connect('file_hashes.db')
    cursor = conn.cursor()

    for file_path, file_hash in file_hashes.items():
        try:
            cursor.execute('INSERT INTO file_hashes (file_path, hash) VALUES (?, ?)', (file_path, file_hash))
        except sqlite3.IntegrityError:
            print(f"Duplicate entry: {file_path}")

    conn.commit()
    conn.close()

# Usage example
file_hashes = get_windows_file_hashes()

create_database()
insert_file_hashes(file_hashes)

#########################################################################################################################

def compute_file_hash(file_path):
    hasher = hashlib.sha256()

    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hasher.update(chunk)

    return hasher.hexdigest()

def check_file_hashes():
    i = 0
    system32_dir = 'C:\\Windows\\System32'
    conn = sqlite3.connect('file_hashes.db')
    cursor = conn.cursor()

    for root, _, files in os.walk(system32_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            if any(file_name.startswith(exclude_file[:-5]) and file_name.endswith(exclude_file[-4:])
                   for exclude_file in EXCEPTIONS):
                continue

            if file_path in EXCEPTIONS:
                print("Excepting by file path: " + file_path)
                continue
            if any(file_path.endswith(extension) for extension in EXCEPTIONS_BY_EXTENSION):
                print("Excepting by extension: " + file_path)
                continue

            try:
                stored_hash = cursor.execute('SELECT hash FROM file_hashes WHERE file_path = ?', (file_path,)).fetchone()

                if stored_hash:
                    file_hash = compute_file_hash(file_path)
                    stored_hash = stored_hash[0]

                    if file_hash != stored_hash:
                        print(f"File is different: {file_path}")
                        print(f"Stored Hash: {stored_hash}")
                        print(f"Current Hash: {file_hash}")
                        bool_hash_change = True
                # else:
                     # print(f"No hash found for file: {file_path}")

            except PermissionError:
                 i += 1

    conn.close()

# Usage example
check_file_hashes()

def send_toast_if_changes_detected():
    if (bool_hash_change):
        show_notification("Some file hashes have changed Ⓧ", image_path)
    else:
        show_notification("File hashes matched ✔", image_path)

send_toast_if_changes_detected()

# def is_windows_update_running():
#     for proc in psutil.process_iter(['name']):
#         if proc.info['name'] == 'wuauclt.exe':  # Windows Update process name
#             return True
#     return False
#
# # Wait for Windows Update to start
# while not is_windows_update_running():
#     time.sleep(1)
#
# print("Windows Update started")
#
# # Wait for Windows Update to finish
# while is_windows_update_running():
#     time.sleep(1)
#
# print("Windows Update finished")
