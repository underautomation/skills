# UnderAutomation.Staubli.Common

## FileConnectParameters

`class FileConnectParameters : FileConnectParametersBase`

Connection parameters of the file client (robot.File). With a real controller, the files are accessed through the FTP server of the controller, with the user and the password of these parameters. With a controller emulated by Staubli Robotics Suite, give the path of its .controller file as addres...

- `FileConnectParameters()`
- `const int DEFAULT_PORT = 21`: Default port of the FTP server
- `const int DEFAULT_TIMEOUT_MS = 30000`: Default timeout of the FTP connection and of the transfers, in milliseconds
- `bool Enable { get; set; }`: Should use this service (default: false)
- Inherited from [FileConnectParametersBase](UnderAutomation.Staubli.Files.Internal.md#fileconnectparametersbase): `User`, `Password`, `Port`, `TimeoutMs`

## SoapConnectParameters

`class SoapConnectParameters : SoapConnectParametersBase`

SOAP connection parameters for communicating with the Staubli robot controller.

- `SoapConnectParameters()`
- `const int DEFAULT_PORT = 851`: Default port of the SOAP server of a real controller (851), used when Port is 0
- `bool Enable { get; set; }`: Should use this service (default: true)
- Inherited from [SoapConnectParametersBase](UnderAutomation.Staubli.Soap.Internal.md#soapconnectparametersbase): `User`, `Password`, `Port`
