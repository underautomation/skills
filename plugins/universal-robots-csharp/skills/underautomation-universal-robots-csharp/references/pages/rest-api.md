# REST API (PolyScope X)

Control a UR cobot with PolyScope X over HTTP: power, brakes, load, play and stop programs, read the program state. Replaces the Dashboard Server.

Web page: https://underautomation.com/universal-robots/documentation/rest-api

The REST API of PolyScope X controls a Universal Robots cobot over HTTP: power, brakes, load and play programs, read the state of the program. This page shows how to use it with the SDK. It replaces the Dashboard Server, which PolyScope X does not have.

For CB-Series and e-Series robots with PolyScope 5, use the [Dashboard Server](remote-commands.md).

## Prerequisites

- The robot runs PolyScope X, or URSim PolyScope X: see [Develop without a robot](configure-offline-simulator.md).
- The robot is in remote control. Switch it with the icon at the top right of PolyScope X. The default password is `operator`.

![Remote control on PolyScope X](https://underautomation.com/universal-robots/switch-remote-polyscopex.png)

## Example

The REST API is disabled by default: set `Rest.Enable` in `ConnectParameters`.

```csharp
using UnderAutomation.UniversalRobots;

class RestQuickStart
{
  static void Main(string[] args)
  {
    var robot = new UR();

    var parameters = new ConnectParameters("192.168.0.1");

    // The REST API is disabled by default
    parameters.Rest.Enable = true;

    // The Dashboard Server does not exist on PolyScope X
    parameters.Dashboard.Enable = false;

    robot.Connect(parameters);

    robot.Rest.PowerOn();
    robot.Rest.BrakeRelease();
    robot.Rest.LoadProgram("my_program");
    robot.Rest.Play();

    // Playing, Paused, Stopped or Unknown
    var state = robot.Rest.GetProgramState();
    Console.WriteLine(state.Value.State);

    robot.Disconnect();
  }
}
```

The same client works without `UR`:

```csharp
using UnderAutomation.UniversalRobots.Rest;

class RestDirect
{
  static void Main(string[] args)
  {
    // A REST client, without a UR instance
    var client = new RestClient();

    // Address of the robot. Optional: port, API version, timeout
    client.Enable("192.168.0.1");

    client.PowerOn();
    client.LoadProgram("my_program");
    client.Play();

    client.Disable();
  }
}
```

## Connection parameters

| Property    | Default  | Role                                 |
| ----------- | -------- | ------------------------------------ |
| `Enable`    | `false`  | Enable the REST client               |
| `Port`      | `80`     | HTTP port of the robot               |
| `Version`   | `Latest` | Version of the API (`V1`, `Latest`)  |
| `TimeoutMs` | `5000`   | Timeout of a request, in ms          |

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Rest;

class RestConnectParameters
{
  static void Main(string[] args)
  {
    var robot = new UR();

    var parameters = new ConnectParameters("192.168.0.1");

    parameters.Rest.Enable = true;
    parameters.Rest.Port = 80;                        // HTTP port, 80 by default
    parameters.Rest.Version = RestApiVersion.V1;      // Latest by default
    parameters.Rest.TimeoutMs = 10000;                // 5000 ms by default

    robot.Connect(parameters);

    // The client is ready
    if (robot.Rest.Initialized)
      Console.WriteLine(robot.Rest.IP + ":" + robot.Rest.Port);
  }
}
```

## Commands

### State of the robot

`PowerOn`, `BrakeRelease`, `PowerOff`, `UnlockProtectiveStop` and `RestartSafety` change the state of the robot. `ChangeRobotState` does the same with a `RobotStateAction`.

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Rest;

class RestRobotState
{
  static void Main(string[] args)
  {
    var robot = new UR();
    robot.Connect(new ConnectParameters("192.168.0.1") { Rest = { Enable = true } });

    // Power on, then release the brakes
    robot.Rest.PowerOn();
    robot.Rest.BrakeRelease();

    // After a protective stop or a safety fault
    robot.Rest.UnlockProtectiveStop();
    robot.Rest.RestartSafety();

    robot.Rest.PowerOff();

    // The same actions, with one generic method
    robot.Rest.ChangeRobotState(RobotStateAction.POWER_ON);
    robot.Rest.ChangeRobotState(RobotStateAction.BRAKE_RELEASE);
  }
}
```

### Programs

`LoadProgram` loads a program by its name, with or without the `.urp` extension. `Play`, `Pause`, `Resume` and `Stop` control it, and `GetProgramState` returns its state: `Playing`, `Paused`, `Stopped` or `Unknown`. `ChangeProgramState` does the same with a `ProgramStateAction`.

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Rest;

class RestProgram
{
  static void Main(string[] args)
  {
    var robot = new UR();
    robot.Connect(new ConnectParameters("192.168.0.1") { Rest = { Enable = true } });

    // The name of the program, with or without .urp
    robot.Rest.LoadProgram("my_program");

    robot.Rest.Play();
    robot.Rest.Pause();
    robot.Rest.Resume();
    robot.Rest.Stop();

    // The same actions, with one generic method
    robot.Rest.ChangeProgramState(ProgramStateAction.play);

    RestApiResponse<ProgramStateResponse> response = robot.Rest.GetProgramState();
    if (response.Succeed)
    {
      RestProgramState state = response.Value.State; // Playing, Paused, Stopped, Unknown
    }
  }
}
```

## Responses and errors

Every method returns a `RestApiResponse`. `GetProgramState` returns a `RestApiResponse<ProgramStateResponse>`, with the state in `Value`.

| Property      | Role                                       |
| ------------- | ------------------------------------------ |
| `Succeed`     | `true` when the robot answered HTTP 200    |
| `StatusCode`  | HTTP status of the answer                  |
| `Message`     | Message of success, or description of the error |
| `RawResponse` | Body of the answer, in JSON                |
| `Value`       | Typed value (`RestApiResponse<T>` only)    |

The errors of the SDK, a timeout for example, raise `InternalErrorOccured`.

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Rest;

class RestResponse
{
  static void Main(string[] args)
  {
    var robot = new UR();
    robot.Connect(new ConnectParameters("192.168.0.1") { Rest = { Enable = true } });

    RestApiResponse response = robot.Rest.PowerOn();

    if (!response.Succeed)
    {
      // HTTP status, message and body of the answer of the robot
      Console.WriteLine(response.StatusCode);
      Console.WriteLine(response.Message);
      Console.WriteLine(response.RawResponse);
    }

    // Errors of the SDK, for example a timeout
    robot.Rest.InternalErrorOccured += (sender, e) =>
    {
      Console.WriteLine(e.Message);
      Console.WriteLine(e.Exception);
    };
  }
}
```

## From the Dashboard Server to the REST API

An application that supports both PolyScope 5 and PolyScope X enables the client of the robot:

```csharp
using UnderAutomation.UniversalRobots;

class RestFromDashboard
{
  static void Main(string[] args)
  {
    var robot = new UR();

    // PolyScope 5 and CB-Series: Dashboard Server
    robot.Connect(new ConnectParameters("192.168.0.1") { Dashboard = { Enable = true } });
    robot.Dashboard.PowerOn();
    robot.Dashboard.LoadProgram("/programs/my_program.urp");
    robot.Dashboard.Play();

    // PolyScope X: REST API
    robot.Connect(new ConnectParameters("192.168.0.1") { Rest = { Enable = true } });
    robot.Rest.PowerOn();
    robot.Rest.LoadProgram("my_program");
    robot.Rest.Play();
  }
}
```

- The REST API uses HTTP (port 80), the Dashboard Server TCP (port 29999).
- `LoadProgram` takes the name of the program, without its folder.
- `ReleaseBrake` of the Dashboard Server is `BrakeRelease` in the REST API.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**RestClientBase** ([reference](../api/UnderAutomation.UniversalRobots.Rest.Internal.md#restclientbase-robotrest))

- `RestApiResponse BrakeRelease()`: Release the robot brakes.
- `RestApiResponse ChangeProgramState(ProgramStateAction action)`: Change the program state. PUT /program/v1/state
- `RestApiResponse ChangeRobotState(RobotStateAction action)`: Change the robot's operational state. PUT /robotstate/v1/state
- `void Disable()`: Disable the REST client
- `RestApiResponse<ProgramStateResponse> GetProgramState()`: Get the current program state. GET /program/v1/state
- `string IP { get; }`: IP address of the robot
- `bool Initialized { get; }`: Indicates whether the REST client has been initialized
- `RestApiResponse LoadProgram(string programName)`: Load a program by name. PUT /program/v1/load
- `RestApiResponse Pause()`: Pause the running program.
- `RestApiResponse Play()`: Start playing the loaded program.
- `int Port { get; }`: HTTP port for REST API
- `RestApiResponse PowerOff()`: Power off the robot.
- `RestApiResponse PowerOn()`: Power on the robot.
- `RestApiResponse RestartSafety()`: Restart the safety system.
- `RestApiResponse Resume()`: Resume a paused program.
- `RestApiResponse Stop()`: Stop the running program.
- `int TimeoutMs { get; }`: Request timeout in milliseconds
- `RestApiResponse UnlockProtectiveStop()`: Unlock the robot from protective stop state.
- `RestApiVersion Version { get; }`: REST API version being used
- Inherited from [URServiceBase](../api/UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

**RestApiResponse** ([reference](../api/UnderAutomation.UniversalRobots.Rest.md#restapiresponse))

- `RestApiResponse()`
- `string Message { get; set; }`: Response message or error description
- `string RawResponse { get; set; }`: Raw JSON response body
- `HttpStatusCode StatusCode { get; set; }`: HTTP status code returned by the API
- `bool Succeed { get; set; }`: Indicates whether the API call succeeded (HTTP 200)

**RobotStateAction** ([reference](../api/UnderAutomation.UniversalRobots.Rest.md#robotstateaction))

- BRAKE_RELEASE: Releases the robot brakes
- POWER_OFF: Powers off the robot
- POWER_ON: Powers on the robot
- RESTART_SAFETY: Restarts the safety system
- UNLOCK_PROTECTIVE_STOP: Unlocks the robot from a protective stop state

**ProgramStateAction** ([reference](../api/UnderAutomation.UniversalRobots.Rest.md#programstateaction))

- pause: Pause the running program
- play: Start or resume playing the program
- resume: Resume a paused program
- stop: Stop the running program

**RestProgramState** ([reference](../api/UnderAutomation.UniversalRobots.Rest.md#restprogramstate))

- Paused: Program is paused
- Playing: Program is playing
- Stopped: Program is stopped
- Unknown: Unknown state

## What to read next

- [Run a program](how-to-run-program.md): the steps from power on to the end of the program.
- [RTDE](rtde.md): the data of the robot, also on PolyScope X.
