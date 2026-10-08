# Licensing

The 30 day trial of the Universal Robots SDK, the license key, the license states, the maintenance and the source license.

Web page: https://underautomation.com/universal-robots/documentation/license

This page explains the licensing of the Universal Robots SDK: the 30 day trial, the license key, the license states and the maintenance. The SDK is a commercial product. Every feature is available during the trial.

## Trial period

The trial starts the first time the library is used on a machine and lasts 30 days. Nothing has to be registered, and no feature is disabled during the trial.

`UR.LicenseInfo` gives the current state. `EvaluationDaysLeft` is the number of days left, and becomes negative when the trial has expired.

## Register a license

Buy a license ([see pricing](https://underautomation.com/order)): you receive a license key and the name of your organization (the licensee). Pass both to the static method `RegisterLicense` of `UR`, once, before the first connection.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.license.license_state import LicenseState
from UnderAutomation.UniversalRobots.License import InvalidLicenseException

# Register the license once, before the first connection.
# The returned object describes the state of the license
info = UR.register_license("YourCompanyName", "YOUR_LICENSE_KEY")

# Number of trial days remaining
evaluation_days_left = info.evaluation_days_left

license_valid = info.state == LicenseState.Licensed

# A readable description of the current state
print(info)

# Check the license once at startup, rather than catching
# the exception on every connection
if not info.is_licensed:
    print(info)
    raise SystemExit(0)

try:
    robot = UR()
    robot.connect("192.168.0.1")
except InvalidLicenseException as ex:
    # The exception comes from the .NET runtime, so its members keep their original names
    print(ex.Message)
    print(ex.LicenseInfo.State)
```

The registration is static: it applies to the whole application, not to one `UR`. It also applies to the clients used without `UR` (`RtdeClient`, `DashboardClient`...). You can register a key after the end of the trial.

`LicenseInfo.ToString()` gives a readable description of the state. It is the message of an `InvalidLicenseException`.

## License states

| `LicenseState`      | Meaning                                                          | The library runs |
| ------------------- | ---------------------------------------------------------------- | ---------------- |
| `None`              | No key is registered and no trial could be started               | no               |
| `Trial`             | The 30 day trial is running                                      | yes              |
| `ExtraTrial`        | An extended trial key is registered                              | yes              |
| `Expired`           | The trial is over                                                | no               |
| `Invalid`           | The licensee and the key do not match                            | no               |
| `MaintenanceNeeded` | The key is valid, but this release is newer than its maintenance | no               |
| `Licensed`          | The product is licensed                                          | yes              |

`IsLicensed` is `true` for `Licensed`, `Trial` and `ExtraTrial`.

## Maintenance

A license includes a number of maintenance years. `MaintenanceExpirationDate` is the last date of the releases that the key can use. A release published after this date reports `MaintenanceNeeded`. The releases you already use keep working: a new key is only needed to use a newer release.

## Without a valid license

`Connect` checks the license before it opens the connection. Without a valid license, it throws an `InvalidLicenseException`. The message says why, and the `LicenseInfo` property of the exception gives the full state.

Test `IsLicensed` once at startup, as in the code above, rather than catching the exception at each connection.

## Source license

The Standard and Pro licenses deliver the obfuscated DLL. The Source license also delivers the full C# code of the library and its Visual Studio solution, to change and build it yourself, within the limits of the [license agreement](https://underautomation.com/universal-robots/eula).

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**LicenseInfo** ([reference](../api/underautomation.universal_robots.license.md#licenseinfo))

- `LicenseInfo(licenseIdentifier: str, licenseKey: str)`: Create a new LicenseInfo instance to retrieve informations about a pair of identifier/key This class should not be used to register your product. Please use static function RegisterLicense to specify your license.
- `is_licensed: bool (read only)`: True if the license state is Licensed, Trial or ExtraTrial ; false otherwise
- `license_key: str (read only)`: The license key supplied by UnderAutomation (null for trial period)
- `product: str (read only)`: Commercial name of this .NET Software library
- `evaluation_days_left: int | None (read only)`: Remaining days of the trial period. Null if the product is licensed. It could be negative if the trial period is ended since several days.
- `evaluation_start_date: datetime (read only)`: The date the trial period starts. If the product is licensed, the date of the library first use.
- `licensee: str (read only)`: Name of your organisation
- `trial_period_expiration_date: datetime | None (read only)`: The date the product will expire. Null if the product is licensed.
- `state: LicenseState (read only)`: The current license state
- `product_release_date: datetime (read only)`: The date this version of the product was released.
- `maintenance_years: int (read only)`: Number of maintenance years included in your license
- `license_issued_date: datetime | None (read only)`: The date you get the license
- `maintenance_expiration_date: datetime | None (read only)`: The date your maintenance contract end and you no longer can use this license with newer versions.

**LicenseState** ([reference](../api/underautomation.universal_robots.license.md#licensestate))

- None_: No license has been provided
- Invalid: The pair License Identifier and License Key are incompatible, you cannot use the library
- Trial: The library is in a trial period, you can use the library
- ExtraTrial: The library is in an extra trial period, you can use the library
- Expired: The trial period as expired, you no more can use the library
- MaintenanceNeeded: Your license does not allow you to use such a recent release. Please buy maintenance to use this version
- Licensed: Congratulations, the library is licensed.

**InvalidLicenseException** ([reference](../api/underautomation.universal_robots.license.md#invalidlicenseexception))

- `LicenseInfo: LicenseInfo (read only)`: The license that causes this exception
- Inherited from System.Exception: `Message`, `InnerException`
