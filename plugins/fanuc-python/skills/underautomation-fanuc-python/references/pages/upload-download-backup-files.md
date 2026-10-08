# Upload, download & backup files

Transfer TP programs, variable files, and backups between your PC and a Fanuc controller using FTP or CGTP.

Web page: https://underautomation.com/fanuc/documentation/upload-download-backup-files

Upload, download, and backup controller files on your Fanuc robot using FTP and CGTP.

## FTP : Full file management

FTP provides complete file management: upload, download, delete, rename, and directory operations.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = ""
parameters.ftp.ftp_password = ""
robot.connect(parameters)

# Upload a TP program to the controller
robot.ftp.direct_file_handling.upload_file_to_controller("C:/Programs/MyPrg.tp", "md:/MyPrg.tp")

# Download a file from the robot
robot.ftp.direct_file_handling.download_file_from_controller("C:/Backup/Backup.va", "md:/Backup.va")

# Delete a file
robot.ftp.direct_file_handling.delete_file("md:/OldProgram.tp")

# List files in a directory
items = robot.ftp.direct_file_handling.get_listing("md:/")
for item in items:
    print(f"{item.name} ({item.type})")

# Create a directory
robot.ftp.direct_file_handling.create_directory("md:/NewFolder")

# Rename a file
robot.ftp.direct_file_handling.rename("md:/old.tp", "md:/new.tp")

# Check file existence
exists = robot.ftp.direct_file_handling.file_exists("md:/MyPrg.tp")
```

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Backup: list all files and download
files = robot.ftp.direct_file_handling.get_listing("md:/")
for file in files:
    robot.ftp.direct_file_handling.download_file_from_controller(f"backup/{file.name}", f"md:/{file.name}")

# Upload a .tp file
robot.ftp.direct_file_handling.upload_file_to_controller("C:/programs/MY_PROGRAM.tp", "md:/MY_PROGRAM.tp")

# Download specific variable files
robot.ftp.direct_file_handling.download_file_from_controller("backup/numreg.va", "md:/numreg.va")
robot.ftp.direct_file_handling.download_file_from_controller("backup/posreg.va", "md:/posreg.va")

# Or use convenience methods
regs = robot.ftp.known_variable_files.get_numreg_file()
```

## CGTP : File download via HTTP

CGTP provides file listing and download through the robot's web server:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# List TP programs
programs = robot.cgtp.http.list_tp_programs()

# Download a file as string
content = robot.cgtp.http.download_as_string("numreg.va")

# Download a file as bytes
data = robot.cgtp.http.download_as_bytes("posreg.va")

# List files via CGTP protocol
files = robot.cgtp.list_files("MD:")
```

See also: [CGTP Alarms, comments & files](cgtp-alarms-files.md)

## Protocol comparison

| Feature | FTP | CGTP |
|---------|-----|------|
| **Upload** | Yes | No |
| **Download** | Yes | Yes |
| **Delete** | Yes | Only jobs |
| **Rename** | Yes | Only jobs |
| **Directory ops** | Yes | No |
| **List files** | Yes | Yes |
| **Authentication** | Optional | Optional |
