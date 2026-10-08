# TP editor with breakpoints

Prototype your own TP Editor with syntax highlighting and breakpoint debugging using Telnet and FTP features.

Web page: https://underautomation.com/fanuc/documentation/tp-editor-with-breakpoints

This article shows how to set breakpoints in TP and Karel programs of a Fanuc controller from a PC, and how to build a small TP editor with breakpoints, using the Telnet and FTP features of the Fanuc SDK.

Fanuc controllers support breakpoints, but the TP editor of ROBOGUIDE and the teach pendant do not show them. With breakpoints, a program stops at a given line, without flags or other synchronization in the program.

<p align="center">
  ![Fanuc TP Editor with breakpoints](https://underautomation.com/fanuc/winforms/editor-with-breakpoints.gif)
</p>

## Breakpoints

### What a breakpoint does

A breakpoint pauses a program at a given line, so that you can look at the state of the robot and of the variables. A program can have several breakpoints, in TP and in Karel programs.

### Add and remove breakpoints

Telnet KCL manages the breakpoints:

- `FanucRobot.Telnet.AddBreakpoint`: adds a breakpoint at a line.
- `FanucRobot.Telnet.GetBreakpoints`: lists the breakpoints of a program.
- `FanucRobot.Telnet.RemoveAllBreakpoints`: removes all the breakpoints of a program.

The controller removes the breakpoints of a task when the task is aborted.

### Example

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

# Create a new Fanuc robot instance
robot = FanucRobot()

# Set connection parameters
parameters = ConnectionParameters("192.168.0.1")
parameters.telnet.enable = True
parameters.telnet.telnet_kcl_password = "TELNET_PASS"

# Connect to the robot
robot.connect(parameters)

# Add a breakpoint at line 10 of TP or Karel program MyProgram
robot.telnet.add_breakpoint("MyProgram", 10)

# List all breakpoints of TP program MyProgram
result = robot.telnet.get_breakpoints("MyProgram")
for breakpoint in result.breakpoints:
    print(f"Breakpoint at line {breakpoint.line}")

# Remove all breakpoints of TP program MyProgram
robot.telnet.remove_all_breakpoints("MyProgram")
```

## A TP editor with breakpoints

### Components

The demo application has a TP editor with breakpoints, written with Windows Forms:

- a `TreeView` that lists the `*.ls` files of the controller;
- a `RichTextBox` with the syntax highlighting of TP code;
- a margin that sets the breakpoints, shows the line being executed, and numbers the lines from the `/MN` section;
- buttons to save and run the program.

### SDK features used

It uses the [FTP features](ftp.md) of the SDK to:

- list the files;
- read the `*.ls` files;
- upload the modified programs;
- monitor the tasks in the background: task names, call stacks and current line.

And the [Telnet features](telnet.md) to start and stop the program, and to run it line by line.

### Source and video

The source is the C# class [TPEditorControl](https://github.com/underautomation/Fanuc.NET/blob/main/UnderAutomation.Fanuc.Showcase.Forms/Components/TPEditorControl.cs) of the [demo application](demo-app.md).

<p align="center">
  <iframe
    width="560"
    height="315"
    style={{ maxWidth: '100%' }}
    src="https://www.youtube.com/embed/Wxxd21P8NLM"
    title="TP editor with breakpoints"
    frameBorder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowFullScreen="true"
  ></iframe>
</p>

### Limits of the demo

- Karel programs are not edited.
- The call stack is simplified: the demo assumes that the task and the program are the same.

## Reference

**BreakpointsResult** ([reference](../api/underautomation.fanuc.common.kcl.md#breakpointsresult))

- `BreakpointsResult()`
- `breakpoints: typing.List[Breakpoint] (read only)`: Gets the breakpoints set on the task.
- Inherited from [Result](../api/underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

**Breakpoint** ([reference](../api/underautomation.fanuc.common.kcl.md#breakpoint))

- `Breakpoint()`
- `line: int (read only)`: Gets the line number where the breakpoint is set.

**AddBreakpointResult** ([reference](../api/underautomation.fanuc.common.kcl.md#addbreakpointresult))

- `AddBreakpointResult()`
- Inherited from [Result](../api/underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

**RemoveBreakpointResult** ([reference](../api/underautomation.fanuc.common.kcl.md#removebreakpointresult))

- `RemoveBreakpointResult()`
- Inherited from [Result](../api/underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`
