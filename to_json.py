import json


def to_json(entries):

    # Load existing data from the JSON file
    try:
        with open("../../AppData/Roaming/JetBrains/PyCharmCE2023.1/scratches/file_info.json", "r") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    # Extend the existing data with the new entries
    existing_data.extend(entries)

    # Write the updated data to the JSON file
    with open("../../AppData/Roaming/JetBrains/PyCharmCE2023.1/scratches/file_info.json", "w") as file:
        json.dump(existing_data, file, indent=4)
