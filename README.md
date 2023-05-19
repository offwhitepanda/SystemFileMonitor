# SystemFileMonitor

As this main.py file stands currently it runs as a demo where it collects the file hashes and then 30 seconds later it checks them again.

### Prepare environment

open PowerShell or Windows Terminal as an Administrator and run prepare_environment.ps1
close the terminal when finished

### Download code

download the zip folder
create a folder on your desktop called "SystemFileChecker"
copy the contents of the download to the "SystemFileChecker" folder so that the structure looks like this

SystemFileChecker<br>
\- main.py<br>
\- check_file_hashes.py<br>
\- etc<br>

### You will need to pip install a few libraries in the project directory:

open PowerShell or Windows Terminal as an Administrator<br>
change directory to the SystemFileChecker folder<br>

#### run:

python.exe -m pip install --upgrade pip<br>
pip install plyer<br>

#### usage examples:

###### main.py intitializes and creates the db and does a test check after 30 seconds
python.exe main.py<br>
###### check_file_hashes simply re-checks file hashes (db must be created already)
python -m check_file_hashes.py<br>



