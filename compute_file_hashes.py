import hashlib


def compute_file_hash(file_path):
    hasher = hashlib.sha256()

    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hasher.update(chunk)

    return hasher.hexdigest()
