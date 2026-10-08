# underautomation.universal_robots.rtde.internal

## RtdeClientBase (robot.rtde)

`from underautomation.universal_robots.rtde.internal.rtde_client_base import RtdeClientBase`

Base class common to all RTDE clients

- `protocol_version_received(handler)`: Event raised during connection when the robot specifies if asked protocol version is supported
- `text_message_received(handler)`: Event raised when a RTDE message is received
- `output_data_received(handler)`: Event raised when data from the robot is comming at specified frequency
- `setup_outputs_received(handler)`: Event raised during connection when the robot acknowledges output setup
- `setup_inputs_received(handler)`: Event raised during connection when the robot acknowledges input setup
- `start_received(handler)`: Event raised as soon as data streaming starts
- `pause_received(handler)`: Event raised when streaming is paused
- `package_received(handler)`: Generic event raised each time a RTDE package is received
- `pause() -> None`: Pause data streaming without disconnecting client
- `resume() -> None`: Restart data streaming after a Pause
- `write_inputs(inputValues: RtdeInputValues) -> None`: Write data to controller. Data must be those selected in connect parameters
- `disconnect() -> None`: Close the RTDE connection to the robot
- `last_text_message: RtdeTextMessageEventArgs (read only)`: Last text received from the robot
- `state: RTDEStates (read only)`: Current RTDE state
- `connected: bool (read only)`: Gets a value indicating if RTDE client is connected to the robot
- `ip: str (read only)`: IP address of the robot
- `applied_frequency: float (read only)`: Output data frequency requested to the robot, only for RTDE version 2
- `version: RtdeVersions (read only)`: Current protocol version used to stream data
- `output_setup: typing.List[RtdeOutputSetupItem] (read only)`: List of all data sent from the robot to the PC (robot point of view)
- `input_setup: typing.List[RtdeInputSetupItem] (read only)`: List of all data the PC can write to the robot (robot point of view)
- `output_recipe_id: int (read only)`: Recipe Identifier of output received data
- `input_recipe_id: int (read only)`: Recipe Identifier of input sent data
- `input_recipe_is_valid: bool (read only)`: Indicates that the recipe is valid, i.e. that all the registers have been found and are not already reserved for writing by another RTDE client. Check event SetupInputsReceived to see which registers are NOT_FOUND or IN_USE
- `measured_frequency: float (read only)`: Measured output data packet frequency. "Timestamp" output data shoud be part of output setup to measure frequency.
- `output_data_values: RtdeOutputValues (read only)`: Last data received from the robot
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## RtdeParametersBase

`from underautomation.universal_robots.rtde.internal.rtde_parameters_base import RtdeParametersBase`

Base parameters to set up RTDE

- `frequency: float`: For RTDE version 2, you can specify a frequency for output received data. Maximum frequency depends on your robot version. If you set frequency to 0, maximum frequency will be choosen Default value is 10Hz
- `version: RtdeVersions`: RTDE version. If set to Auto, the most recent version will be choosen according to your robot version Default value is V2
- `output_setup: RtdeOutputSetup`: List of all output data the robot will send to your application
- `input_setup: RtdeInputSetup`: List of all input data you can send to the robot
- `port: int`: TCP port used for RTDE connection. Default : 30004
- `static DEFAULT_PORT: int`: Default RTDE TCP port used (30004)

## RtdeSetup2

`from underautomation.universal_robots.rtde.internal.rtde_setup_2 import RtdeSetup2`

Base class for an RTDE recipe, a collection of T setup items that describe which RTDE variables to exchange.

- `add(data: U, index: int=0) -> T`: Adds a variable to the recipe with the specified register index.
- `add(data: U) -> T`: Adds a variable to the recipe with register index 0.
- `remove(data: U, index: int=-1) -> int`: Removes all items matching the specified variable and optionally a specific register index.
- `contains(data: U, index: int=0) -> bool`: Determines whether the recipe contains the specified variable at the given register index.
- `contains(data: U) -> bool`: Determines whether the recipe contains the specified variable at any register index.
- `to_distinct_list() -> typing.List[T]`: Returns a deduplicated array of setup items, removing duplicates by data and index.

## RtdeSetupItem1

`from underautomation.universal_robots.rtde.internal.rtde_setup_item_1 import RtdeSetupItem1`

Abstract base class representing a single RTDE variable in a recipe, identified by an enum value of type T and an optional register index.

- `RtdeSetupItem1(data: T, index: int)`: Initializes a new instance for the specified RTDE variable and register index.
- `index: int`: Gets or sets the register index for array/register RTDE variables. Defaults to 0.
- `data: T`: Gets or sets the enum value identifying the RTDE variable.
- `description: RtdeDataDescription1[T] (read only)`: Gets the description metadata for this variable (name, type, array info).
- `name: str (read only)`: Gets the RTDE protocol name for this variable, including the register index suffix for array variables.
- `type: RtdeTypes (read only)`: Gets the RTDE wire type of this variable.
- `protocol_type: str (read only)`: Gets the uppercase RTDE protocol type string sent on the wire during setup.
