# Kinematics models and DH parameters

Get the DH parameters of a Yaskawa robot from the catalog of 169 models, from the ALL.PRM file of the controller, or from your own values.

Web page: https://underautomation.com/yaskawa/documentation/kinematics-models

This page shows the three ways to get the geometry of a Yaskawa Motoman arm for the offline kinematics of the SDK: the catalog of 169 models, the `ALL.PRM` parameter file of the controller, or your own DH parameters. It also explains the meaning of each parameter.

## DH parameters

`DhParameters` holds the 9 values that change from one 6-axis Yaskawa arm to another. The other values of the Denavit-Hartenberg table are the same for every arm.

![The lengths of a GP7, drawn at zero pulse. A1 to A3 and D4 to D6 are in mm. D5 is 0 on a robot with a spherical wrist.](https://underautomation.com/yaskawa/documentation/diagrams/kinematics-dh-parameters.svg)

| Parameter | Meaning                                                        | GP7  |
| --------- | -------------------------------------------------------------- | ---- |
| `A1`      | Offset between the S axis and the L axis, along the arm (mm)   | 40   |
| `A2`      | Lower arm: L axis to U axis (mm)                               | 445  |
| `A3`      | Elbow offset: U axis to the forearm axis (mm)                  | 40   |
| `D4`      | Forearm: U axis to the wrist (mm)                              | 440  |
| `D5`      | Wrist offset along the B axis (mm). 0 for a spherical wrist    | 0    |
| `D6`      | Wrist to flange, along the T axis (mm)                         | 80   |
| `Theta2`  | DH angle of the L axis at zero pulse (degrees)                 | -90  |
| `Theta3`  | DH angle of the U axis at zero pulse (degrees)                 | 0    |
| `Theta5`  | DH angle of the B axis at zero pulse (degrees)                 | 0    |

The parameters use the modified DH convention (Craig). `KinematicsCategory` tells which solver is used: `Opw` when `D5` is 0, `J5OffsetWrist` otherwise.

## From the catalog

`ArmKinematicModels` lists 169 models: GP (33), MH (48), ES (14), SP (14), HC (15), HP (7), AR (6), MS (6), PH (5), MotoMINI and others. `FromArmKinematicModel` returns their parameters. `FromArmKinematicModelName` finds a model by its name, and returns `null` when the name is not known.

```python
from underautomation.yaskawa.common.dh_parameters import DhParameters
from underautomation.yaskawa.kinematics.arm_kinematic_models import ArmKinematicModels
from underautomation.yaskawa.kinematics.kinematics_utils import KinematicsUtils

# From the enumeration: 169 models of the catalog
gp7 = DhParameters.from_arm_kinematic_model(ArmKinematicModels.GP7)

# From the name of the model, case ignored. None if the model is not known.
hc10 = DhParameters.from_arm_kinematic_model_name("HC10")

print(gp7)                            # A1=40, A2=445, A3=40, D4=440, D5=0, D6=80...
print(gp7.kinematics_category.name)   # Opw
print(hc10.kinematics_category.name)  # J5OffsetWrist

# Every model of the catalog
for model in ArmKinematicModels:
    print(model.name)
```

Some models have several variants, with the order code in the name (for example `HC10DT_1_06VXHC10_B10`). Use the variant of the name plate of your robot. Do not store the integer value of the enumeration: new models are added in alphabetical order and shift the values. Store the name.

## From the controller

The `ALL.PRM` file of a controller contains the geometry of its robot. `FromPrmFile` reads a file saved on the PC, `FromPrmContent` the text of the file. DX100, DX200, FS100, YRC1000 and YRC1000micro files are supported. The parameters of the first robot (R1) are read.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.common.dh_parameters import DhParameters
from underautomation.yaskawa.kinematics.kinematics_utils import KinematicsUtils

# ALL.PRM saved from the controller, on the PC
from_file = DhParameters.from_prm_file(r"C:\Backup\ALL.PRM")

# Or downloaded from the controller (1.4 MB, about 13 s on a YRC1000micro)
parameters = ConnectParameters("192.168.0.1")
parameters.ftp.enable = True
robot = YaskawaRobot()
robot.connect(parameters)

content = robot.ftp.get_file("ALL.PRM")
dh = DhParameters.from_prm_content(content)

# Joint solutions of the current position (tool 0, robot frame)
position = robot.high_speed_e_server.get_robot_cartesian_position()
for solution in KinematicsUtils.inverse_kinematics(position, dh):
    print(solution)

robot.disconnect()
```

Download `ALL.PRM` with [FTP](ftp-transfer.md), [HTTP](http.md) or the [High Speed Ethernet Server](hses-files.md). The file is about 1.4 MB: FTP and HTTP take about 13 s on a YRC1000micro, the High Speed Ethernet Server about 45 s. Save it once, then use `FromPrmFile`.

On a MotoMINI, the parameters read from `ALL.PRM` are equal to `ArmKinematicModels.MotoMINI` of the catalog. The file is the right choice for a model that is not in the catalog, or to check the model of a robot.

A file of a robot with a structure that is not supported throws a `NotSupportedException`. See [Supported robots](kinematics.md#supported_robots).

## Your own values

The constructor takes `A1`, `A2`, `A3`, `D4`, `D5`, `D6` in mm, then `Theta2`, `Theta3`, `Theta5` in degrees. Two `DhParameters` with the same values are equal.

```python
from underautomation.yaskawa.common.dh_parameters import DhParameters
from underautomation.yaskawa.kinematics.arm_kinematic_models import ArmKinematicModels

# A1, A2, A3, D4, D5, D6 in mm, then Theta2, Theta3, Theta5 in degrees
dh = DhParameters(40, 445, 40, 440, 0, 80, -90, 0, 0)

# Same values as the catalog: the same geometry
same_as_gp7 = dh == DhParameters.from_arm_kinematic_model(ArmKinematicModels.GP7)

# The solver is chosen from the values: D5 = 0 is a spherical wrist
print(dh.kinematics_category.name)  # Opw
```

`DhParameters` implements `IDhParameters`: your own class can also implement this interface and be passed to `KinematicsUtils`.

## Reference

**DhParameters** ([reference](../api/underautomation.yaskawa.common.md#dhparameters))

- `DhParameters(a1: float, a2: float, a3: float, d4: float, d5: float, d6: float, theta2: float, theta3: float, theta5: float)`: Initializes a new instance of DhParameters with the specified values.
- `static from_arm_kinematic_model_name(modelName: str) -> 'DhParameters'`: Returns the DH parameters of a known robot model, from its name (for example "GP7" or "HC10DTP"). The comparison ignores case.
- `static from_arm_kinematic_model(model: ArmKinematicModels) -> 'DhParameters'`: Returns the DH parameters of a known robot model.
- `static from_prm_file(path: str) -> 'DhParameters'`: Reads the DH parameters of robot group 1 from an ALL.PRM parameter file saved from a controller. DX100, DX200, FS100, YRC1000 and YRC1000micro files are supported.
- `static from_prm_content(content: str) -> 'DhParameters'`: Reads the DH parameters of robot group 1 from the text content of an ALL.PRM parameter file. DX100, DX200, FS100, YRC1000 and YRC1000micro files are supported.
- `a1: float`
- `a2: float`
- `a3: float`
- `d4: float`
- `d5: float`
- `d6: float`
- `theta2: float`
- `theta3: float`
- `theta5: float`
- `kinematics_category: KinematicsCategory (read only)`: Kinematic structure of the arm: Opw when d5 is 0, J5OffsetWrist otherwise.

**IDhParameters** ([reference](../api/underautomation.yaskawa.common.md#idhparameters))

- `a1: float (read only)`: Offset between the S axis and the L axis, along the arm (mm).
- `a2: float (read only)`: Lower arm length, between the L axis and the U axis (mm).
- `a3: float (read only)`: Elbow offset, between the U axis and the forearm axis (mm).
- `d4: float (read only)`: Forearm length, between the U axis and the wrist (mm).
- `d5: float (read only)`: Wrist offset along the B axis (mm). Zero for a spherical wrist.
- `d6: float (read only)`: Distance between the wrist and the flange, along the T axis (mm).
- `theta2: float (read only)`: DH angle of the L axis when the L axis is at zero pulse (degrees).
- `theta3: float (read only)`: DH angle of the U axis when the U axis is at zero pulse (degrees).
- `theta5: float (read only)`: DH angle of the B axis when the B axis is at zero pulse (degrees).

**ArmKinematicModels** ([reference](../api/underautomation.yaskawa.kinematics.md#armkinematicmodels))

- AR1440: AR1440
- AR1730: AR1730
- AR2010: AR2010
- AR3120: AR3120
- AR700: AR700
- AR900: AR900
- DX1350D: DX1350D
- EP4000D: EP4000D
- EPH130D: EPH130D
- EPH400D: EPH400D
- EPX1250: EPX1250
- ES0165D_A00: ES0165D-A00
- ES0165D_A10: ES0165D-A10
- ES0165D_B00: ES0165D-B00
- ES0165D_B10: ES0165D-B10
- ES0165D_Z10: ES0165D-Z10
- ES0200D: ES0200D
- ES0280D: ES0280D
- ES165RD: ES165RD
- ES200D: ES200D
- ES200RD_A00_Proto: ES200RD-A00-Proto
- ES200RD_A10: ES200RD-A10
- ES200RD_J00: ES200RD-J00
- ES200RD_Pack_Proto: ES200RD-Pack-Proto
- ES280D: ES280D
- GA50: GA50
- GG250: GG250
- GP110: GP110
- GP110H: GP110H
- GP12: GP12
- GP165R: GP165R
- GP180: GP180
- GP180H: GP180H
- GP180_120: GP180-120
- GP200R: GP200R
- GP200S: GP200S
- GP20HL: GP20HL
- GP215: GP215
- GP225: GP225
- GP225H: GP225H
- GP25: GP25
- GP250: GP250
- GP25SV: GP25SV
- GP25_12: GP25-12
- GP280: GP280
- GP280L: GP280L
- GP300R: GP300R
- GP35H: GP35H
- GP35L: GP35L
- GP360: GP360
- GP4: GP4
- GP400: GP400
- GP400R: GP400R
- GP50: GP50
- GP600: GP600
- GP7: GP7
- GP70L: GP70L
- GP8: GP8
- GP88: GP88
- GP8L: GP8L
- HC10: HC10
- HC10DTF: HC10DTF
- HC10DTFP: HC10DTFP
- HC10DTP: HC10DTP
- HC10DT_1_06VXHC10_A10: HC10DT_1-06VXHC10-A10
- HC10DT_1_06VXHC10_B10: HC10DT_1-06VXHC10-B10
- HC10DT_1_06VXHC10_B11: HC10DT_1-06VXHC10-B11
- HC10DT_1_06VXHC10_B12: HC10DT_1-06VXHC10-B12
- HC10DT_1_06VXHC10_C11: HC10DT_1-06VXHC10-C11
- HC10SDTP: HC10SDTP
- HC20DT: HC20DT
- HC20DTP: HC20DTP
- HC20SDT: HC20SDT
- HC20SDTP: HC20SDTP
- HC30PL: HC30PL
- HP0020D_A00: HP0020D-A00
- HP0020D_A10: HP0020D-A10
- HP0020D_B00: HP0020D-B00
- HP0020D_B10: HP0020D-B10
- HP0020F: HP0020F
- HP0165D: HP0165D
- HP020RD: HP020RD
- MA02010: MA02010
- MA03120: MA03120
- MA1440: MA1440
- MC02000: MC02000
- MCL0020: MCL0020
- MCL020F: MCL020F
- MH00005: MH00005
- MH00006_A00: MH00006-A00
- MH00006_A30: MH00006-A30
- MH00006_B00: MH00006-B00
- MH00006_B30: MH00006-B30
- MH00006_C00: MH00006-C00
- MH0000J: MH0000J
- MH00024_A00: MH00024-A00
- MH00024_A10: MH00024-A10
- MH00024_Z00_Proto: MH00024-Z00-Proto
- MH0003F: MH0003F
- MH00050_A00: MH00050-A00
- MH00050_A10: MH00050-A10
- MH00050_A20: MH00050-A20
- MH00050_B00: MH00050-B00
- MH00050_B10: MH00050-B10
- MH00050_B20: MH00050-B20
- MH00050_J00: MH00050-J00
- MH00050_J10: MH00050-J10
- MH00050_J20: MH00050-J20
- MH00050_Z00: MH00050-Z00
- MH0005F: MH0005F
- MH0005L: MH0005L
- MH0005S: MH0005S
- MH0006F: MH0006F
- MH0006S: MH0006S
- MH00080: MH00080
- MH00165_A00: MH00165-A00
- MH00165_A10: MH00165-A10
- MH00165_B00: MH00165-B00
- MH00200: MH00200
- MH00215: MH00215
- MH00250: MH00250
- MH00280: MH00280
- MH003BM: MH003BM
- MH00400: MH00400
- MH005BM: MH005BM
- MH005LF: MH005LF
- MH005LS: MH005LS
- MH00600: MH00600
- MH006SF: MH006SF
- MH00900: MH00900
- MH110: MH110
- MH12: MH12
- MH180_A00: MH180-A00
- MH180_A10: MH180-A10
- MH180_C00: MH180-C00
- MH225: MH225
- MHP045L: MHP045L
- MPL0080: MPL0080
- MPX1150: MPX1150
- MPX1400: MPX1400
- MPX1950: MPX1950
- MS00080: MS00080
- MS00120: MS00120
- MS0080W: MS0080W
- MS100: MS100
- MS165: MS165
- MS210: MS210
- MotoMINI: MotoMINI
- PH130F: PH130F
- PH130RF: PH130RF
- PH13RLD: PH13RLD
- PH200R: PH200R
- PH200RF: PH200RF
- SP100: SP100
- SP110H: SP110H
- SP130: SP130
- SP150R: SP150R
- SP165: SP165
- SP165_105: SP165-105
- SP180H: SP180H
- SP180H_110: SP180H-110
- SP185R: SP185R
- SP210: SP210
- SP225H: SP225H
- SP225H_135: SP225H-135
- SP235: SP235
- SP80: SP80
- UP0350D: UP0350D
- UP400RD: UP400RD

## What to read next

- [Offline kinematics](kinematics.md): forward and inverse kinematics.
- [FTP file transfers](ftp-transfer.md): download `ALL.PRM` and the other files of the controller.
