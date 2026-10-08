# UnderAutomation.Staubli.Soap

## SoapClient

`class SoapClient : SoapClientBase`

SOAP client for Staubli robots

- `SoapClient()`: Create a new instance of SoapClient
- `void Connect(string ip, string user, string password, int port)`: Connect to a robot
- Inherited from [SoapClientBase](UnderAutomation.Staubli.Soap.Internal.md#soapclientbase-controllersoap): `Disconnect`, `GetRobots`, `GetCurrentCartesianJointPosition`, `GetCurrentJointPosition`, `GetControllerParameters`, `GetValApplications`, `GetJointRange`, `GetAllPhysicalIos`, `GetDhParameters`, `GetTasks`, `ReadIos`, `StartApplication`, `StopAndUnloadAll`, `StopApplication`, `TaskKill`, `TaskResume`, `TaskSuspend`, `WriteIos`, `LoadProject`, `ForwardKinematics`, `ReverseKinematics`, `MoveC`, `MoveJC`, `MoveJJ`, `MoveL`, `ResetMotion`, `RestartMotion`, `StopMotion`, `SetPower`, `Ip`, `Port`, `SessionId`, `Enabled`
