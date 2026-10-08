# underautomation.staubli.soap

## SoapClient

`from underautomation.staubli.soap.soap_client import SoapClient`

SOAP client for Staubli robots

- `SoapClient()`: Create a new instance of SoapClient
- `connect(ip: str, user: str, password: str, port: int) -> None`: Connect to a robot
- Inherited from [SoapClientBase](underautomation.staubli.soap.internal.md#soapclientbase-controllersoap): `disconnect`, `get_robots`, `get_current_cartesian_joint_position`, `get_current_joint_position`, `get_controller_parameters`, `get_val_applications`, `get_joint_range`, `get_all_physical_ios`, `get_dh_parameters`, `get_tasks`, `read_ios`, `start_application`, `stop_and_unload_all`, `stop_application`, `task_kill`, `task_resume`, `task_suspend`, `write_ios`, `load_project`, `forward_kinematics`, `reverse_kinematics`, `move_c`, `move_jc`, `move_jj`, `move_l`, `reset_motion`, `restart_motion`, `stop_motion`, `set_power`, `ip`, `port`, `session_id`, `enabled`
