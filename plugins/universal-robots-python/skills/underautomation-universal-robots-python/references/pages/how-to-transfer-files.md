# Transfer files and backups

Copy the programs of a UR cobot to a PC for a backup, send a program to the robot and load it, in C# or Python with SFTP.

Web page: https://underautomation.com/universal-robots/documentation/how-to-transfer-files

This article shows how to copy the programs of a Universal Robots cobot to a PC for a backup, and how to send a program to the robot and load it, in C# or Python. The files are transferred with SFTP, then loaded with the Dashboard Server or the REST API.

## Which way to choose

| Task                              | SDK                                                         |
| --------------------------------- | ----------------------------------------------------------- |
| List the programs                 | SFTP `EnumeratePrograms()`, `EnumerateInstallations()`, `ListDirectory()` |
| Download, upload a file           | SFTP `DownloadFile()`, `UploadFile()`                       |
| Load a program sent by SFTP       | Dashboard Server `LoadProgram()`, REST API `LoadProgram()`  |
| Read or change a program on the PC| `URProgram.Load()`, `URInstallation.Load()`                 |
| Archive a folder on the robot     | SSH `RunCommand("tar ...")`, then SFTP                      |

The programs are in `/programs` on a robot, and in `/home/ur/ursim-current/programs` on URSim. A program uses an installation (`.installation`): copy both.

## Prerequisites

- Secure Shell is enabled on the robot. On PolyScope, open `Settings`, `Security`, `Secure Shell`.
- The Linux user: `root` on a robot, `ur` on URSim, password `easybot` by default.
- To load the program, the robot is in remote control.

## Example

The program copies the programs folder of the robot, with its subfolders, into a dated folder of the PC. Then it sends a program and its installation, and loads the program.

```python
import os
from datetime import datetime
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters

# /programs on a robot, /home/ur/ursim-current/programs on URSim
ROBOT_PROGRAMS = "/programs/"

# Copy a folder of the robot and its subfolders
def download(robot, remote_folder, local_folder):
    os.makedirs(local_folder, exist_ok=True)
    for item in robot.sftp.list_directory(remote_folder):
        if item.name in (".", ".."):
            continue
        local = os.path.join(local_folder, item.name)
        if item.is_directory:
            download(robot, item.full_name + "/", local)
        else:
            robot.sftp.download_file(item.full_name, local)

robot = UR()

parameters = ConnectParameters("192.168.0.1")
parameters.ssh.enable_sftp = True
parameters.ssh.username = "root"  # "ur" on URSim
parameters.ssh.password = "easybot"

# Primary Interface and Dashboard Server stay enabled, to load the program
robot.connect(parameters)

# 1. Backup: copy the programs folder of the robot to the PC
backup = os.path.join("C:\\backups", datetime.now().strftime("%Y%m%d-%H%M%S"))
download(robot, ROBOT_PROGRAMS, backup)

# 2. Send a program and its installation to the robot
robot.sftp.upload_file("C:\\work\\pick_and_place.urp", ROBOT_PROGRAMS + "pick_and_place.urp")
robot.sftp.upload_file("C:\\work\\default.installation", ROBOT_PROGRAMS + "default.installation")

# 3. Load it in PolyScope
load = robot.dashboard.load_program("pick_and_place.urp")
print("Loaded" if load.succeed else load.message)

robot.disconnect()
```

## Notes

- A full backup of the controller (the system, the URCaps, the logs) is made with the backup function of PolyScope, or with a USB key. This article copies the programs and the installations.
- `UploadFile` replaces a file with the same name. Copy the old file first if you need it.
- A program sent while it is loaded in PolyScope is not reloaded: call `LoadProgram` again.

## Troubleshooting

- **`ConnectException` for SFTP:** Secure Shell is disabled, or the user or the password is wrong (the inner exception is then an `SshAuthenticationException`). On a robot, the user is `root`.
- **`SftpPathNotFoundException`:** the folder does not exist. On URSim, the programs are in `/home/ur/ursim-current/programs`.
- **`LoadProgram` fails:** the robot is not in remote control, or the path is wrong.

## What to read next

- [SFTP](sftp-file-handling.md): the operations of the client.
- [Program and installation files](archive-file.md): change a program on the PC.
- [Run a program](how-to-run-program.md).
