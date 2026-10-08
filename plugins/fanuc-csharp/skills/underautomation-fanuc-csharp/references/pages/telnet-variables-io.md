# Variables & I/O via Telnet

Read and write system variables, set output ports, simulate and unsimulate input ports using Telnet KCL.

Web page: https://underautomation.com/fanuc/documentation/telnet-variables-io

> **Telnet KCL is a legacy protocol.** It is not secured: the password and the commands are sent in clear text. It is hard to maintain: the answers of the controller change with the firmware version, and ROBOGUIDE behaves differently from a real controller. The KCL commands of `robot.Telnet` are also available with `robot.Cgtp.Kcl`, through the web server of the controller (firmware V8.30 and later), without Telnet setup. Prefer it for new developments: see [KCL commands over CGTP](cgtp-kcl.md).

Read and write system variables, set output ports, simulate and unsimulate input ports using Telnet KCL.

## Read and write variables

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Telnet;

public class TelnetVariablesIoRead
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Telnet.Enable = true;
        parameters.Telnet.TelnetKclPassword = "TELNET_PASS";
        robot.Connect(parameters);

        // Read a variable
        GetVariableResult result = robot.Telnet.GetVariable("$RMT_MASTER");
        string value = result.RawValue;

        // Write a variable
        robot.Telnet.SetVariable("$RMT_MASTER", 1);
        robot.Telnet.SetVariable("$MCR.$GENOVERRIDE", 50);
        robot.Telnet.SetVariable("$[MY_PROG]my_var", "hello");

        // Get current pose
        GetCurrentPoseResult pose = robot.Telnet.GetCurrentPose();
    }
}
```

You can read any system variable, program variable, or user-defined variable by name. The value must match the declared data type. Use brackets (`[]`) after the variable name to specify an array element.

## Set and simulate I/O ports

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Telnet;

public class TelnetVariablesIoPorts
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Telnet.Enable = true;
        parameters.Telnet.TelnetKclPassword = "TELNET_PASS";
        robot.Connect(parameters);

        // Set an output port (DOUT port 2 = OFF)
        robot.Telnet.SetPort(KCLPorts.DOUT, 2, 0);

        // Set an output port (DOUT port 5 = ON)
        robot.Telnet.SetPort(KCLPorts.DOUT, 5, 1);

        // Simulate an input port (DIN port 3 = ON)
        robot.Telnet.Simulate(KCLPorts.DIN, 3, 1);

        // Stop simulating DIN port 3
        robot.Telnet.Unsimulate(KCLPorts.DIN, 3);

        // Stop simulating all ports
        robot.Telnet.UnsimulateAll();
    }
}
```

## Available port types

The `KCLPorts` enum defines the available port types:

| Port | Description |
|------|-------------|
| `DIN` / `DOUT` | Digital Input / Output |
| `GIN` / `GOUT` | Group Input / Output |
| `AIN` / `AOUT` | Analog Input / Output |
| `OPIN` / `OPOUT` | Operator Panel Input / Output |
| `RDI` / `RDO` | Robot Digital Input / Output |
| `WDI` / `WDO` | Weld Digital Input / Output |
| `PLCIN` / `PLCOUT` | PLC Input / Output |
| `FLAG` | Flag register |

## Complete example

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Telnet;

public class TelnetVariablesIo
{
  static void Main()
  {
    FanucRobot robot = new FanucRobot();
    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Telnet.Enable = true;
    parameters.Telnet.TelnetKclPassword = "TELNET_PASS";
    robot.Connect(parameters);

    // Read a system variable
    GetVariableResult result = robot.Telnet.GetVariable("$RMT_MASTER");
    string value = result.RawValue;

    // Write system variables
    robot.Telnet.SetVariable("$RMT_MASTER", 1);
    robot.Telnet.SetVariable("$MCR.$GENOVERRIDE", 50);

    // Get current TCP pose
    GetCurrentPoseResult pose = robot.Telnet.GetCurrentPose();

    // Set an output port
    robot.Telnet.SetPort(KCLPorts.DOUT, 2, 0);
    robot.Telnet.SetPort(KCLPorts.DOUT, 5, 1);

    // Simulate an input port
    robot.Telnet.Simulate(KCLPorts.DIN, 3, 1);

    // Stop simulating a port
    robot.Telnet.Unsimulate(KCLPorts.DIN, 3);

    // Stop simulating all ports
    robot.Telnet.UnsimulateAll();
  }
}
```

## API reference

**GetVariableResult** ([reference](../api/UnderAutomation.Fanuc.Common.Kcl.md#getvariableresult))

- `GetVariableResult()`
- `GenericVariable ParseResult()`: Returns a structured object which represents the variable (not supported with Telnet)
- `string RawValue { get; }`: Gets the raw value of the variable as a string.
- Inherited from [Result](../api/UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

**SetVariableResult** ([reference](../api/UnderAutomation.Fanuc.Common.Kcl.md#setvariableresult))

- `SetVariableResult()`
- Inherited from [SetValueResult](../api/UnderAutomation.Fanuc.Common.Kcl.md#setvalueresult): `FormerValue`, `NewValue`
- Inherited from [Result](../api/UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

**SetPortResult** ([reference](../api/UnderAutomation.Fanuc.Common.Kcl.md#setportresult))

- `SetPortResult()`
- Inherited from [SetValueResult](../api/UnderAutomation.Fanuc.Common.Kcl.md#setvalueresult): `FormerValue`, `NewValue`
- Inherited from [Result](../api/UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

**SimulateResult** ([reference](../api/UnderAutomation.Fanuc.Common.Kcl.md#simulateresult))

- `SimulateResult()`
- Inherited from [Result](../api/UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

**KCLPorts** ([reference](../api/UnderAutomation.Fanuc.Common.Kcl.md#kclports))

- AIN: Analog Input port.
- AOUT: Analog Output port.
- DIN: Digital Input port.
- DOUT: Digital Output port.
- GIN: General Input port.
- GOUT: General Output port.
- OPOUT: Operator Panel Output port.
- RDO: Robot Digital Output port.
- TPOUT: Teach Pendant Output port.
- WDI: Weld Digital Input port.
- WDO: Weld Digital Output port.
