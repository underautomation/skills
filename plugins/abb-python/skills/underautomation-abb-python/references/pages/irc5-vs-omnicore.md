# IRC5 or OmniCore: which RWS version

RWS 1.0 runs on IRC5 with RobotWare 6, RWS 2.0 on OmniCore with RobotWare 7. Compare both, and see what changes in your code.

Web page: https://underautomation.com/abb/documentation/irc5-vs-omnicore

An IRC5 controller speaks RWS 1.0, an OmniCore controller speaks RWS 2.0. You tell the SDK which one with the `RwsVersion` enum at connection time, and the rest of your code stays the same. This page compares the two, and lists the few places where the difference is visible.

## Which controller do you have

The controller generation, the RobotWare version and the RWS version always go together. You cannot run RWS 2.0 on an IRC5, and RobotWare 7 only exists on OmniCore.

|                    | IRC5            | OmniCore        |
| ------------------ | --------------- | --------------- |
| RobotWare          | 6.x and earlier | 7.x and later   |
| RWS version        | 1.0             | 2.0             |
| `RwsVersion` value | `Irc5_V1_0`     | `OmniCore_V2_0` |

If you do not know, look at the RobotWare version on the teach pendant, or read it with `robot.Rws.System.GetInfo().Version` once you are connected.

HTTP versus HTTPS is a separate question from the RWS version. Both generations can be configured for either one, it depends on the controller's own network setup, not on its generation. Check that on the controller and set `UseHttps` to match. When the controller answers on HTTPS with a self-signed certificate, the SDK accepts it without any extra step.

## Choosing the version in your code

`OmniCore_V2_0` is the default.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.connection_parameters import ConnectionParameters
from underautomation.abb.rws.rws_version import RwsVersion

# IRC5 controller, RobotWare 6 : RWS 1.0
irc5 = ConnectionParameters("192.168.0.1")
irc5.rws.version = RwsVersion.Irc5_V1_0

# OmniCore controller, RobotWare 7 : RWS 2.0
omni_core = ConnectionParameters("192.168.0.2")
omni_core.rws.version = RwsVersion.OmniCore_V2_0

# use_https is independent of the version. Set it to match how this
# particular controller is configured on the network, not its generation.
omni_core.rws.use_https = True

robot = AbbController()
robot.connect(omni_core)

# The same code then works on both controllers
print(robot.rws.system.get_info().version)
```

A wrong version does not produce a clear error. The connection opens, then the first request answers with the HTTP status code 404 and the SDK throws an `RwsException`. If you see a 404 on a call that should exist, check `RwsVersion` first.

## Detecting the version at runtime

The controller does not announce its RWS version, so a tool that has to work with a fleet of unknown robots tries one version and falls back on the other. `robot.Rws.Version` gives back the version the connection was opened with.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.connection_parameters import ConnectionParameters
from underautomation.abb.rws.rws_version import RwsVersion
from UnderAutomation.ABB.Rws import RwsException

def open_controller(ip):
    robot = AbbController()

    omni_core = ConnectionParameters(ip)
    omni_core.rws.version = RwsVersion.OmniCore_V2_0
    omni_core.rws.use_https = True

    try:
        robot.connect(omni_core)
        robot.rws.system.get_info()  # the first real request tells whether the guess was right
        return robot
    except RwsException as error:
        if error.StatusCode != 404:
            raise
        robot.disconnect()

    irc5 = ConnectionParameters(ip)
    irc5.rws.version = RwsVersion.Irc5_V1_0
    irc5.rws.use_https = False

    robot.connect(irc5)
    return robot

# The version is a connection parameter, the controller does not announce it.
# Try RWS 2.0 first, fall back to RWS 1.0 when the controller answers 404.
robot = open_controller("192.168.0.1")

print(robot.rws.version)  # Irc5_V1_0 or OmniCore_V2_0

info = robot.rws.system.get_info()
print(info.name)     # name of the system
print(info.version)  # RobotWare version, 6.x on IRC5, 7.x on OmniCore

robot.disconnect()
```

## What changes in your code

Almost nothing. One method covers both versions, and the SDK sends what the connected controller expects. `robot.Rws.Rapid.GetSymbolValue(...)`, `robot.Rws.Io.SetSignalValue(...)` and `robot.Rws.MotionSystem.GetRobTarget(...)` are written once.

Three behaviours differ enough to be worth knowing.

**Mastership domains.** The two generations do not cut the controller the same way. IRC5 has three domains, `Configuration`, `Rapid` and `Motion`. OmniCore has two, `Edit`, which covers the system parameters and the RAPID programs together, and `Motion`. You can pass any of the four values of `MastershipDomain` on either controller, the SDK maps them onto the domains the controller really has.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain

robot = AbbController()
robot.connect("192.168.0.1")

# Domains the connected controller really exposes
for domain in robot.rws.mastership.get_domains():
    print(domain)

# Motion is needed to move a mechanical unit
robot.rws.mastership.request(MastershipDomain.Motion)
robot.rws.mastership.release(MastershipDomain.Motion)

# Edit covers the system parameters and the RAPID programs at once
robot.rws.mastership.request(MastershipDomain.Edit)
robot.rws.mastership.release(MastershipDomain.Edit)

# Some writes need more than one domain. A domain is taken one at a time, so take
# the ones the controller exposes to hold everything.
for domain in robot.rws.mastership.get_domains():
    robot.rws.mastership.request(domain)

for domain in robot.rws.mastership.get_domains():
    robot.rws.mastership.release(domain)

robot.disconnect()
```

**Implicit mastership.** On OmniCore, `Panel.SetSpeedRatio` and `Controller.Restart` need the mastership. Both take it for you, use it and give it back, which is the default. On IRC5 the same two calls need no mastership, and the flag is ignored. See the [mastership page](rws-mastership.md).

**Long lists.** OmniCore answers a long list in pages. The SDK asks for the following pages and gives you the complete array, so a directory with 2000 files comes back whole. IRC5 answers everything in one response. In both cases you get one `T[]`, only the number of HTTP requests changes.

## Operations that exist on one version only

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes. Everything not listed here works on both.

| Operation                                                                                              | Available on | Behaviour on the other version                           |
| ------------------------------------------------------------------------------------------------------ | ------------ | -------------------------------------------------------- |
| `Elog.GetMessage` by sequence number alone                                                             | OmniCore     | `RwsException`, name the domain of the message           |
| `Controller.GetTimeServer(serverIp)`                                                                   | OmniCore     | `RwsException`, call `GetTimeServer()` without argument  |
| `Controller.SetIdentity(name, id)`, the `id` argument                                                  | IRC5         | sent as provided, the controller may ignore or refuse it |
| `Io.PulseSignal` and `Io.SendDeviceCommand`, the value length                                          | IRC5         | not used, the controller computes it                     |
| `Rapid.LoadModule`, the name of what was loaded                                                        | OmniCore     | returns null, the module is loaded anyway                |
| `Rapid.SetProgramPointerToRoutine`, the module name, and `SetProgramPointerToCursor`, the routine name | IRC5         | the controller works them out on its own                 |
| `Controller.RestoreBackup`, the controller settings                                                    | IRC5         | RobotWare 7 ignores the flag                             |

## Data filled in by one version only

Some properties are always there, but only one controller generation fills them. The others stay null, or keep their `Unknown` value.

| Property                                                       | Filled by |
| -------------------------------------------------------------- | --------- |
| `BackupSystemInfo.RobotWareVersion`                            | IRC5      |
| `BackupSystemInfo.RobotControlVersion`, `.RobotOsVersion`      | OmniCore  |
| `NetworkInterfaceItem.Network`, `.PrimaryDns`, `.SecondaryDns` | OmniCore  |
| `SafetyConfiguration.ConfigurationStatus`                      | OmniCore  |
| `TimeServerInfo.Time`                                          | OmniCore  |
| `RapidTaskInfo.ExecutionCycle`                                 | OmniCore  |
| `IoClientAction` returned by `Io.SetNetworkConfigurationType`  | OmniCore  |
| `RapidModuleText.DeclaredLength`                               | OmniCore  |

A virtual controller in RobotStudio behaves like the real one it simulates, with one exception: `SystemInfo` keeps the detailed version numbers, the title, the type and the build date empty on a simulated system. That is a property of the machine, not of the RWS version.

## Which one should you target

If you write a tool for one cell, target the controller you have. If you write a product, support both: the code is the same, and the only work is to let the user choose the version, or to detect it as shown above. Test against two RobotStudio virtual controllers, one RobotWare 6 and one RobotWare 7.

## Going further

- [Connect to your robot](connect.md), the full list of connection parameters
- [Mastership](rws-mastership.md), the domains and the write lock
- [Robot Web Services overview](rws.md), the nine services
- [Test with a RobotStudio virtual controller](virtual-controller.md)

**RwsVersion** ([reference](../api/underautomation.abb.rws.md#rwsversion-robotrwsversion))

- Irc5_V1_0: RWS 1.0, exposed by IRC5 controllers running RobotWare 6 and earlier.
- OmniCore_V2_0: RWS 2.0, exposed by OmniCore controllers running RobotWare 7 and later. This is the default when no version is specified.

**RwsConnectParameters** ([reference](../api/underautomation.abb.rws.md#rwsconnectparameters))

- `RwsConnectParameters()`
- `enable: bool`: Enable or disable the RWS client connection
- `static DEFAULT_PORT: int`: Default RWS port (80 for HTTP, 443 for HTTPS)
- `static DEFAULT_USERNAME: str`: Default username for Digest Authentication
- `static DEFAULT_PASSWORD: str`: Default password for Digest Authentication
- `static DEFAULT_TIMEOUT: int`: Default timeout in milliseconds
- Inherited from [RwsConnectParametersBase](../api/underautomation.abb.rws.internal.md#rwsconnectparametersbase): `port`, `username`, `password`, `timeout`, `use_https`, `version`
