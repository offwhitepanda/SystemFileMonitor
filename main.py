from initialize_db import *
from check_file_hashes import check_file_hashes
from utility_commands import sleep_with_progress

# Initialize Database and Insert File Hashes
create_database()
insert_file_hashes()

# Wait 30 seconds before checking for changes (this is just a test run)
print_colorful("Sleeping for 30 seconds", "green")
sleep_with_progress(30)

# Detect file hash changes
check_file_hashes()
