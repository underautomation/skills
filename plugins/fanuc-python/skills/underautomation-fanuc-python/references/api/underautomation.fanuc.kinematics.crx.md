# underautomation.fanuc.kinematics.crx

## CrxKinematicsUtils

`from underautomation.fanuc.kinematics.crx.crx_kinematics_utils import CrxKinematicsUtils`

Utility methods implementing CRX collaborative robot inverse kinematics using a geometric approach.

- `static inverse_kinematics(pose: CartesianPosition, parameters: DhParameters, includeDuals: bool=True) -> typing.List[JointsPosition]`: Solve IK for a desired tool pose (WPR). Returns up to 16 solutions (including duals, Eq. (23)). This implements Steps 1..7 from paper §2.6 with references to Eqs. (13–23).
