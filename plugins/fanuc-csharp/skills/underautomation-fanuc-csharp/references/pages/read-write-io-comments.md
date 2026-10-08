# Read & write I/O comments

Read and write comments (descriptions) for registers and I/O ports using SNPX or CGTP.

Web page: https://underautomation.com/fanuc/documentation/read-write-io-comments

Read and write descriptive comments (labels) for registers and I/O ports on your Fanuc robot.

## SNPX

SNPX reads and writes comments for all register and I/O types:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Snpx.Internal;
using UnderAutomation.Fanuc.Snpx;

public class ReadWriteIoCommentsSnpx
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Read a comment (default 16 characters)
        string comment = robot.Snpx.Comments.Read(CommentType.Register, 5);

        // Read with custom length (must be even, >= 2)
        string longComment = robot.Snpx.Comments.Read(CommentType.Register, 5, 24);

        // Write a comment
        robot.Snpx.Comments.Write(CommentType.PositionRegister, 1, "Home Position", 16);
        robot.Snpx.Comments.Write(CommentType.DI, 1, "Start Button", 16);
    }
}
```

Available comment types: `Register`, `PositionRegister`, `StringRegister`, `DI`, `DO`, `RI`, `RO`, `UI`, `UO`, `SI`, `SO`, `WI`, `WO`, `WSI`, `WSO`, `GI`, `GO`, `AI`, `AO`, `Flag`.

See also: [SNPX Alarms & task status](snpx-alarms-tasks.md)

## CGTP Web Server

CGTP provides bulk comment reading and individual writing:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;
using UnderAutomation.Fanuc.Common;

public class ReadWriteIoCommentsCgtp
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Read all register comments
        string[] regComments = robot.Cgtp.GetComments(CgtpCommentType.NumericRegister);
        string[] posComments = robot.Cgtp.GetComments(CgtpCommentType.PositionRegister);

        // Write a comment
        robot.Cgtp.SetComment(CgtpCommentType.NumericRegister, 1, "Speed setpoint");

        // Read I/O comments by category
        IOComments digitalIo = robot.Cgtp.GetIoComments(CgtpCommentIoType.DigitalIO);
        IOComments robotIo = robot.Cgtp.GetIoComments(CgtpCommentIoType.RobotIO);
        IOComments groupIo = robot.Cgtp.GetIoComments(CgtpCommentIoType.GroupIO);
        IOComments analogIo = robot.Cgtp.GetIoComments(CgtpCommentIoType.AnalogIO);
    }
}
```

See also: [CGTP Alarms, comments & files](cgtp-alarms-files.md)

## Protocol comparison

| Feature | SNPX | CGTP |
|---------|------|------|
| **Read individual** | Yes | No (bulk only) |
| **Read all** | No | Yes |
| **Write** | Yes | Yes |
| **Register comments** | Yes | Yes |
| **I/O comments** | Yes | Yes (by category) |
| **Custom length** | Yes (even, ≥ 2) | No (fixed) |
