from collections import defaultdict


def import_exceptions():

    # Define the default dictionary with list as the default value
    variable_array_mapping = defaultdict(list)

    # Specify the paths to the exceptions_by_path.txt and exceptions_by_extension.txt files
    file_paths = [
        "exceptions/exceptions_by_path.txt",
        "exceptions/exceptions_by_extension.txt",
        # Add more file paths here if needed
    ]

    # Iterate over each file path
    for file_path in file_paths:
        # Extract the file name without the extension
        file_name = file_path.split("/")[-1].split(".")[0]

        # Open the file and read the lines
        with open(file_path, "r") as file:
            # Remove trailing newline characters and append lines to the corresponding variable array
            variable_array_mapping[file_name].extend(line.rstrip('\n') for line in file)

    return variable_array_mapping
