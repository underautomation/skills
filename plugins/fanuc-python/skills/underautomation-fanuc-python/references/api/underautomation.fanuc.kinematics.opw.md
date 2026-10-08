# underautomation.fanuc.kinematics.opw

## OpwKinematicsUtils

`from underautomation.fanuc.kinematics.opw.opw_kinematics_utils import OpwKinematicsUtils`

Utility methods implementing OPW kinematics for a 6R industrial robot with ortho-parallel base and spherical wrist (so called 3-2-1 structure). This class is a C# implementation of the analytical solution described in: M. Brandstötter et al., "An Analytical Solution of the Inverse Kinematics Prob...

- `static inverse_kinematics(pose: CartesianPosition, dhParameters: DhParameters) -> typing.List[JointsPosition]`: Compute all inverse kinematics solutions for a desired end effector pose using the OPW model and the closed form from the paper. This method is a direct implementation of the "Positioning Part" and "Orientation Part" formulas summarized on page 6 (Table II) of the paper. Steps: 1) Compute wrist c...
