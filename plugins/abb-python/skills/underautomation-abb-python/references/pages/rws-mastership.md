# Mastership

Mastership is the write lock of the controller. Request and release it explicitly, or let the SDK take it implicitly for a single call.

Web page: https://underautomation.com/abb/documentation/rws-mastership

Mastership is the write lock of the controller. Only one client holds it at a time, and a client that does not hold it cannot change anything. Reading never needs it. The service is `robot.Rws.Mastership`.

The mastership belongs to the connection that took it. Every call made through the same `AbbController` is the holder. It stays held until you release it or until the connection ends.

## Domains

The mastership is not global, it is taken per domain. `MastershipDomain` has four values, and the two controller generations do not cut the controller the same way.

| `MastershipDomain` | Covers                                                 | IRC5, RWS 1.0                                 | OmniCore, RWS 2.0     |
| ------------------ | ------------------------------------------------------ | --------------------------------------------- | --------------------- |
| `Motion`           | Jogging, mechanical units, anything that moves an axis | Its own domain                                | Its own domain        |
| `Configuration`    | System parameters of the controller                    | Its own domain                                | Same domain as `Edit` |
| `Rapid`            | RAPID programs and their data                          | Its own domain                                | Same domain as `Edit` |
| `Edit`             | System parameters and RAPID programs together          | Takes `Configuration` and `Rapid` in one call | Its own domain        |

You can ask for any of the four values on any controller. The service maps them onto the domains the connected controller really has. `GetDomains` tells you which ones it exposes.

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

## Request and release

`Request` takes a domain, `Release` gives it back. Without argument, both work on every domain of the controller at once.

Take the mastership as late as possible and give it back as early as possible. While you hold it, the operator of the robot cannot change the same domain from the teach pendant. Put the release in a `finally` block, so a failed write does not leave the lock taken.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain

robot = AbbController()
robot.connect("192.168.0.1")

# Take the write lock of the RAPID domain
robot.rws.mastership.request(MastershipDomain.Rapid)
try:
    robot.rws.rapid.set_symbol_value("RAPID/T_ROB1/user/reg1", "12")
    robot.rws.rapid.set_symbol_value("RAPID/T_ROB1/user/reg2", "34")
finally:
    # Give it back as early as possible, even when the write failed
    robot.rws.mastership.release(MastershipDomain.Rapid)

robot.disconnect()
```

A few points to know:

- `Request` fails when somebody else already holds the domain, and also when this connection already holds it.
- `Release()` without argument is accepted even when nothing is held. It is safe to call in a `finally` block.
- In manual mode, the controller only grants the mastership once the operator has given your client the right to act on their behalf.
- When a value of the enum covers several domains of the connected controller, `Request` takes them all. If one of them is refused, the parts already taken are given back before the error is reported.

## Who holds the mastership

`GetInfo` returns a `MastershipInfo` per domain: who holds it, and whether it is this connection. `HeldByMe` is the property to test before a write.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain
from underautomation.abb.rws.data.mastership_holder import MastershipHolder

robot = AbbController()
robot.connect("192.168.0.1")

# State of every domain of the controller
for domain in robot.rws.mastership.get_domains():
    info = robot.rws.mastership.get_info(domain)
    print(f"{info.domain} : holder {info.holder}, held by me {info.held_by_me}")
    print(f"  application {info.application}, location {info.location}")

# State of a single domain
motion = robot.rws.mastership.get_info(MastershipDomain.Motion)

if motion.holder == MastershipHolder.None_:
    print("Motion is free, it can be taken")
elif not motion.held_by_me:
    print("Somebody else holds Motion, a write would fail with 403")

robot.disconnect()
```

`Holder` is a `MastershipHolder`: `None` when the domain is free, `Remote` for a client on the network, `Local` for a device attached to the controller like the teach pendant, `Internal` when the controller itself holds it during an operation that must not be interrupted.

## Implicit mastership

> **Available on** RWS 1.0 (IRC5) : no | RWS 2.0 (OmniCore) : yes. On IRC5 these calls need no mastership, the flag is ignored.

Two operations take the mastership for you, use it for a single request and give it back immediately: `Panel.SetSpeedRatio` and `Controller.Restart`. This is the default. Pass `false` for the `useImplicitMastership` parameter when your own code already holds the mastership, otherwise the controller refuses the second request on a domain you already hold.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.controller_restart_mode import ControllerRestartMode

robot = AbbController()
robot.connect("192.168.0.1")

# The mastership is taken for this single call and given back right after
robot.rws.panel.set_speed_ratio(50)

# Same behaviour for a restart of the controller
robot.rws.controller.restart(ControllerRestartMode.Restart)

# Set the flag to False when your own code already holds the mastership.
# The .NET API takes every domain in one call, in Python they are taken one by one.
domains = robot.rws.mastership.get_domains()

for domain in domains:
    robot.rws.mastership.request(domain)

try:
    robot.rws.panel.set_speed_ratio(100, False)
finally:
    for domain in domains:
        robot.rws.mastership.release(domain)

robot.disconnect()
```

Every other write operation needs an explicit `Request`.

## What happens without mastership

The controller answers with the HTTP status code 403, and the SDK throws an `RwsException` with `StatusCode` set to 403. The same code is used when the user account lacks the UAS grant, so check the mastership state to tell the two cases apart.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain
from UnderAutomation.ABB.Rws import RwsException

robot = AbbController()
robot.connect("192.168.0.1")

try:
    # No mastership taken, the controller refuses the write
    robot.rws.rapid.set_symbol_value("RAPID/T_ROB1/user/reg1", "5")
except RwsException as ex:
    if ex.StatusCode != 403:
        raise

    # Find out who holds the domain
    info = robot.rws.mastership.get_info(MastershipDomain.Rapid)
    print(f"{info.domain} is held by {info.holder} ({info.application})")

robot.disconnect()
```

Operations that need the mastership:

| Domain          | Examples                                                                                              |
| --------------- | ----------------------------------------------------------------------------------------------------- |
| `Rapid`         | Write a RAPID variable, load or unload a module, start and stop the program, move the program pointer |
| `Motion`        | Jog the robot, change the position of a mechanical unit, calibration operations                       |
| `Configuration` | Change the system parameters, the network configuration, the time zone                                |

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## API reference

**Methods of MastershipService** ([reference](../api/underautomation.abb.rws.services.md#mastershipservice-robotrwsmastership))

- `get_domains() -> typing.List[MastershipDomain]`: Gets the domains the connected controller can give the mastership of (synchronous)
- `get_info(domain: MastershipDomain) -> MastershipInfo`: Gets who holds the mastership of one domain (synchronous)
- `get_info() -> typing.List[MastershipInfo]`: Gets who holds the mastership of every domain of the controller (synchronous)
- `request(domain: MastershipDomain) -> None`: Takes the mastership of one domain (synchronous)
- `request() -> None`: Takes the mastership of every domain of the controller (synchronous)
- `release(domain: MastershipDomain) -> None`: Gives back the mastership of one domain (synchronous)
- `release() -> None`: Gives back the mastership of every domain of the controller (synchronous)

**MastershipInfo** ([reference](../api/underautomation.abb.rws.data.md#mastershipinfo))

- `MastershipInfo()`: Initializes a new instance of the MastershipInfo class
- `domain: MastershipDomain`: Domain this state describes
- `holder: MastershipHolder`: Who holds the mastership of the domain
- `held_by_me: bool`: Whether this connection is the one holding the mastership, and is therefore allowed to write in the domain
- `user_id: int | None`: Identifier the controller gave the user holding the mastership, null when nobody holds it
- `location: str`: Where the holder is, as it declared itself, null when nobody holds the mastership
- `alias: str`: Alternate name of the location of the holder, null when nobody holds the mastership
- `application: str`: Name of the application holding the mastership, null when nobody holds it

**MastershipDomain** ([reference](../api/underautomation.abb.rws.data.md#mastershipdomain))

- Edit: Everything that changes the system itself: its configuration and its RAPID programs. On a connection established with version 1, where the two are separate domains, asking for this one takes and together.
- Motion: The movement of the robot: jogging, the mechanical units and everything that makes an axis move
- Configuration: The system parameters of the controller. On a connection established with version 2, where it is not a domain of its own, this is the same domain as .
- Rapid: The RAPID programs and their data. On a connection established with version 2, where it is not a domain of its own, this is the same domain as .

**MastershipHolder** ([reference](../api/underautomation.abb.rws.data.md#mastershipholder))

- Unknown: The controller reported a holder this library does not know
- None_: Nobody holds the mastership, it is free to be taken
- Remote: A client connected over the network holds it, possibly this one
- Local: A device attached to the controller holds it, the teach pendant for instance
- Internal: The controller itself holds it, while it runs an operation that must not be interrupted
