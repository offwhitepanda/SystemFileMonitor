import sqlite3
from get_file_hashes import get_file_hashes
from utility_commands import print_colorful


def create_database():

    print_colorful("Creating database", "green")
    conn = sqlite3.connect('../../AppData/Roaming/JetBrains/PyCharmCE2023.1/scratches/file_hashes.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS file_hashes
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, file_path TEXT UNIQUE, hash TEXT)''')

    conn.commit()
    conn.close()


def insert_file_hashes():

    files_inserted_count = 0
    duplicate_entry_count = 0

    print_colorful("Retrieving File Hashes", "green")
    file_hashes = get_file_hashes()

    conn = sqlite3.connect('../../AppData/Roaming/JetBrains/PyCharmCE2023.1/scratches/file_hashes.db')
    cursor = conn.cursor()

    print_colorful("Inserting File Hashes", "green")
    for file_path, file_hash in file_hashes.items():
        try:
            cursor.execute('INSERT INTO file_hashes (file_path, hash) VALUES (?, ?)', (file_path, file_hash))
            files_inserted_count += 1
        except sqlite3.IntegrityError:
            duplicate_entry_count += 1

    conn.commit()
    conn.close()
    print(f"Files inserted: {files_inserted_count}")
    print(f"Duplicate entry count: {duplicate_entry_count}")
