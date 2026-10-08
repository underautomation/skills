# underautomation.staubli.common

## FileConnectParameters

`from underautomation.staubli.common.file_connect_parameters import FileConnectParameters`

Connection parameters of the file client (robot.File). With a real controller, the files are accessed through the FTP server of the controller, with the user and the password of these parameters. With a controller emulated by Staubli Robotics Suite, give the path of its .controller file as addres...

- `FileConnectParameters()`
- `enable: bool`: Should use this service (default: false)
- `static DEFAULT_PORT: int`: Default port of the FTP server
- `static DEFAULT_TIMEOUT_MS: int`: Default timeout of the FTP connection and of the transfers, in milliseconds
- Inherited from [FileConnectParametersBase](underautomation.staubli.files.internal.md#fileconnectparametersbase): `user`, `password`, `port`, `timeout_ms`

## SoapConnectParameters

`from underautomation.staubli.common.soap_connect_parameters import SoapConnectParameters`

SOAP connection parameters for communicating with the Staubli robot controller.

- `SoapConnectParameters()`
- `enable: bool`: Should use this service (default: true)
- `static DEFAULT_PORT: int`: Default port of the SOAP server of a real controller (851), used when Port is 0
- Inherited from [SoapConnectParametersBase](underautomation.staubli.soap.internal.md#soapconnectparametersbase): `user`, `password`, `port`
