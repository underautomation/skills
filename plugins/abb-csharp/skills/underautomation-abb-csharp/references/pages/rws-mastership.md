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

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class MastershipDomains
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Domains the connected controller really exposes
        foreach (MastershipDomain domain in robot.Rws.Mastership.GetDomains())
            Console.WriteLine(domain);

        // Motion is needed to move a mechanical unit
        robot.Rws.Mastership.Request(MastershipDomain.Motion);
        robot.Rws.Mastership.Release(MastershipDomain.Motion);

        // Edit covers the system parameters and the RAPID programs at once
        robot.Rws.Mastership.Request(MastershipDomain.Edit);
        robot.Rws.Mastership.Release(MastershipDomain.Edit);

        // Without argument, every domain is taken and given back
        robot.Rws.Mastership.Request();
        robot.Rws.Mastership.Release();

        robot.Disconnect();
    }
}
```

## Request and release

`Request` takes a domain, `Release` gives it back. Without argument, both work on every domain of the controller at once.

Take the mastership as late as possible and give it back as early as possible. While you hold it, the operator of the robot cannot change the same domain from the teach pendant. Put the release in a `finally` block, so a failed write does not leave the lock taken.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class MastershipRequestRelease
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Take the write lock of the RAPID domain
        robot.Rws.Mastership.Request(MastershipDomain.Rapid);
        try
        {
            robot.Rws.Rapid.SetSymbolValue("RAPID/T_ROB1/user/reg1", "12");
            robot.Rws.Rapid.SetSymbolValue("RAPID/T_ROB1/user/reg2", "34");
        }
        finally
        {
            // Give it back as early as possible, even when the write failed
            robot.Rws.Mastership.Release(MastershipDomain.Rapid);
        }

        robot.Disconnect();
    }
}
```

A few points to know:

- `Request` fails when somebody else already holds the domain, and also when this connection already holds it.
- `Release()` without argument is accepted even when nothing is held. It is safe to call in a `finally` block.
- In manual mode, the controller only grants the mastership once the operator has given your client the right to act on their behalf.
- When a value of the enum covers several domains of the connected controller, `Request` takes them all. If one of them is refused, the parts already taken are given back before the error is reported.

## Who holds the mastership

`GetInfo` returns a `MastershipInfo` per domain: who holds it, and whether it is this connection. `HeldByMe` is the property to test before a write.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class MastershipState
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // State of every domain of the controller
        foreach (MastershipInfo info in robot.Rws.Mastership.GetInfo())
        {
            Console.WriteLine($"{info.Domain} : holder {info.Holder}, held by me {info.HeldByMe}");
            Console.WriteLine($"  application {info.Application}, location {info.Location}");
        }

        // State of a single domain
        MastershipInfo motion = robot.Rws.Mastership.GetInfo(MastershipDomain.Motion);

        if (motion.Holder == MastershipHolder.None)
            Console.WriteLine("Motion is free, it can be taken");
        else if (!motion.HeldByMe)
            Console.WriteLine("Somebody else holds Motion, a write would fail with 403");

        robot.Disconnect();
    }
}
```

`Holder` is a `MastershipHolder`: `None` when the domain is free, `Remote` for a client on the network, `Local` for a device attached to the controller like the teach pendant, `Internal` when the controller itself holds it during an operation that must not be interrupted.

## Implicit mastership

> **Available on** RWS 1.0 (IRC5) : no | RWS 2.0 (OmniCore) : yes. On IRC5 these calls need no mastership, the flag is ignored.

Two operations take the mastership for you, use it for a single request and give it back immediately: `Panel.SetSpeedRatio` and `Controller.Restart`. This is the default. Pass `false` for the `useImplicitMastership` parameter when your own code already holds the mastership, otherwise the controller refuses the second request on a domain you already hold.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class MastershipImplicit
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // The mastership is taken for this single call and given back right after
        robot.Rws.Panel.SetSpeedRatio(50);

        // Same behaviour for a restart of the controller
        robot.Rws.Controller.Restart(ControllerRestartMode.Restart);

        // Set the flag to false when your own code already holds the mastership
        robot.Rws.Mastership.Request();
        try
        {
            robot.Rws.Panel.SetSpeedRatio(100, false);
        }
        finally
        {
            robot.Rws.Mastership.Release();
        }

        robot.Disconnect();
    }
}
```

Every other write operation needs an explicit `Request`.

## What happens without mastership

The controller answers with the HTTP status code 403, and the SDK throws an `RwsException` with `StatusCode` set to 403. The same code is used when the user account lacks the UAS grant, so check the mastership state to tell the two cases apart.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws;
using UnderAutomation.ABB.Rws.Data;

public class MastershipDenied
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        try
        {
            // No mastership taken, the controller refuses the write
            robot.Rws.Rapid.SetSymbolValue("RAPID/T_ROB1/user/reg1", "5");
        }
        catch (RwsException ex) when (ex.StatusCode == 403)
        {
            // Find out who holds the domain
            MastershipInfo info = robot.Rws.Mastership.GetInfo(MastershipDomain.Rapid);
            Console.WriteLine($"{info.Domain} is held by {info.Holder} ({info.Application})");
        }

        robot.Disconnect();
    }
}
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

**Methods of MastershipService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#mastershipservice-robotrwsmastership))

- `MastershipDomain[] GetDomains()`: Gets the domains the connected controller can give the mastership of (synchronous)
  - async: `Task<MastershipDomain[]> GetDomainsAsync(CancellationToken cancellationToken = default)`
- `MastershipInfo[] GetInfo()`: Gets who holds the mastership of every domain of the controller (synchronous)
  - async: `Task<MastershipInfo[]> GetInfoAsync(CancellationToken cancellationToken = default)`
  - async: `Task<MastershipInfo> GetInfoAsync(MastershipDomain domain, CancellationToken cancellationToken = default)`
- `MastershipInfo GetInfo(MastershipDomain domain)`: Gets who holds the mastership of one domain (synchronous)
- `void Release()`: Gives back the mastership of every domain of the controller (synchronous)
  - async: `Task ReleaseAsync(CancellationToken cancellationToken = default)`
  - async: `Task ReleaseAsync(MastershipDomain domain, CancellationToken cancellationToken = default)`
- `void Release(MastershipDomain domain)`: Gives back the mastership of one domain (synchronous)
- `void Request()`: Takes the mastership of every domain of the controller (synchronous)
  - async: `Task RequestAsync(CancellationToken cancellationToken = default)`
  - async: `Task RequestAsync(MastershipDomain domain, CancellationToken cancellationToken = default)`
- `void Request(MastershipDomain domain)`: Takes the mastership of one domain (synchronous)

**MastershipInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#mastershipinfo))

- `MastershipInfo()`: Initializes a new instance of the Data.MastershipInfo class
- `string Alias { get; set; }`: Alternate name of the location of the holder, null when nobody holds the mastership
- `string Application { get; set; }`: Name of the application holding the mastership, null when nobody holds it
- `MastershipDomain Domain { get; set; }`: Domain this state describes
- `bool HeldByMe { get; set; }`: Whether this connection is the one holding the mastership, and is therefore allowed to write in the domain
- `MastershipHolder Holder { get; set; }`: Who holds the mastership of the domain
- `string Location { get; set; }`: Where the holder is, as it declared itself, null when nobody holds the mastership
- `long? UserId { get; set; }`: Identifier the controller gave the user holding the mastership, null when nobody holds it

**MastershipDomain** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#mastershipdomain))

- Configuration: The system parameters of the controller. On a connection established with version 2, where it is not a domain of its own, this is the same domain as MastershipDomain.Edit.
- Edit: Everything that changes the system itself: its configuration and its RAPID programs. On a connection established with version 1, where the two are separate domains, asking for this one takes MastershipDomain.Configuration and MastershipDomain.Rapid together.
- Motion: The movement of the robot: jogging, the mechanical units and everything that makes an axis move
- Rapid: The RAPID programs and their data. On a connection established with version 2, where it is not a domain of its own, this is the same domain as MastershipDomain.Edit.

**MastershipHolder** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#mastershipholder))

- Internal: The controller itself holds it, while it runs an operation that must not be interrupted
- Local: A device attached to the controller holds it, the teach pendant for instance
- None: Nobody holds the mastership, it is free to be taken
- Remote: A client connected over the network holds it, possibly this one
- Unknown: The controller reported a holder this library does not know
