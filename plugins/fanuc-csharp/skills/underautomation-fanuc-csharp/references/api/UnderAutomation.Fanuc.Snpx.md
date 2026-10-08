# UnderAutomation.Fanuc.Snpx

## SnpxClient

`class SnpxClient : SnpxClientBase`

SNPX protocol client for communicating with Fanuc robots.

- `SnpxClient()`: Initializes a new instance of the Snpx.SnpxClient class.
- `void Connect(string ip, int port = 60008)`: Connects to a Fanuc robot using the SNPX protocol.
- Inherited from [SnpxClientBase](UnderAutomation.Fanuc.Snpx.Internal.md#snpxclientbase-robotsnpx): `PollAndGetUpdatedConnectedState`, `Disconnect`, `ClearAlarms`, `SetVariable`, `ClearAssignments`, `GetAssignments`, `Ip`, `NumericRegisters`, `NumericRegistersInt32`, `NumericRegistersInt16`, `PositionRegisters`, `StringRegisters`, `IntegerSystemVariables`, `RealSystemVariables`, `PositionSystemVariables`, `StringSystemVariables`, `DigitalSignals`, `SDI`, `SDO`, `RDI`, `RDO`, `UI`, `UO`, `SI`, `SO`, `WI`, `WO`, `WSI`, `PMC_K`, `PMC_R`, `NumericIOs`, `GI`, `GO`, `AI`, `AO`, `PMC_D`, `Flags`, `CurrentPosition`, `CurrentTaskStatus`, `ActiveAlarm`, `AlarmHistory`, `Comments`, `SimulationStatus`, `Language`, `Connected`
