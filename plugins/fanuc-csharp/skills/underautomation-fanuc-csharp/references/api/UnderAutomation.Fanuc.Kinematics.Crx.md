# UnderAutomation.Fanuc.Kinematics.Crx

## CrxKinematicsUtils

`static class CrxKinematicsUtils`

Utility methods implementing CRX collaborative robot inverse kinematics using a geometric approach.

- `static JointsPosition[] InverseKinematics(CartesianPosition pose, DhParameters parameters, bool includeDuals = true)`: Solve IK for a desired tool pose (WPR). Returns up to 16 solutions (including duals, Eq. (23)). This implements Steps 1..7 from paper §2.6 with references to Eqs. (13–23).
