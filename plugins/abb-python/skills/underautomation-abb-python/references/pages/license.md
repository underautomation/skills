# Licensing

To be used, this SDK is subject to licensing. You have 30 days to test it for free.

Web page: https://underautomation.com/abb/documentation/license

This SDK is a commercial product. You have 30 days to test it for free, with every feature available. After that a license key is needed.

## Trial period

The trial starts the first time the library is used on a machine, and lasts 30 days. Nothing has to be registered, and no feature is disabled during that time.

`AbbController.LicenseInfo` tells you where you stand. `EvaluationDaysLeft` counts the days remaining, and becomes negative once the trial has expired.

## Register a license

Buy a license ([see pricing](https://underautomation.com/order)) and we send you a license key with the name of your organization. Pass both to the static method `RegisterLicense` of `AbbController`, once, before the first connection.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.license.license_state import LicenseState
from UnderAutomation.ABB.License import InvalidLicenseException

# Register the license once, before the first connection
AbbController.register_license("YourCompanyName", "YOUR_LICENSE_KEY")

robot = AbbController()
info = robot.license_info

# Number of trial days remaining, None when the product is licensed
evaluation_days_left = info.evaluation_days_left

license_valid = info.state == LicenseState.Licensed

# A readable description of the current state
print(info)

# Check the license once at startup, rather than catching the exception
# on every connection
if not info.is_licensed:
    print(info)
    raise SystemExit(0)

# Without a key the library runs in its 30 day trial period.
# connect raises an InvalidLicenseException once the trial has expired.
try:
    robot = AbbController()
    robot.connect("192.168.0.1")
except InvalidLicenseException as ex:
    # The exception comes from the .NET runtime, so its members keep their original names
    print(ex.Message)
    print(ex.LicenseInfo.State)
```

The registration is static: it applies to the whole application, not to one `AbbController` instance. You can register a key even after the trial period has ended.

`AbbController.LicenseInfo` returns the current state at any moment. Its `ToString()` gives a readable description, which is what an `InvalidLicenseException` carries as its message.

## License states

| `LicenseState`      | Meaning                                                                    | The library runs |
| ------------------- | -------------------------------------------------------------------------- | ---------------- |
| `None`              | No key has been registered and no trial could be started                   | no               |
| `Trial`             | The 30 day trial period is running                                         | yes              |
| `ExtraTrial`        | An extended trial key has been registered                                  | yes              |
| `Expired`           | The trial period is over                                                   | no               |
| `Invalid`           | The organization name and the key do not go together                       | no               |
| `MaintenanceNeeded` | The key is valid, but this release is newer than the maintenance it covers | no               |
| `Licensed`          | The product is licensed                                                    | yes              |

`IsLicensed` is true for `Licensed`, `Trial` and `ExtraTrial`.

A license includes a number of maintenance years. `MaintenanceExpirationDate` is the date up to which a release can be used with that key. Versions released after that date report `MaintenanceNeeded`. The versions you already use keep working, a new key is only needed to move to a newer release.

## What happens without a valid license

`AbbController.Connect` checks the license before opening the connection and throws an `InvalidLicenseException` when it is not valid. The exception message says why, and its `LicenseInfo` property carries the full state.

Test `IsLicensed` at startup rather than catching the exception on every connection, as the code above does.

## Source license

The Standard and Pro licenses deliver the obfuscated DLL. The Source license also delivers the full C# code of the library and its Visual Studio solution, to change and build it yourself, within the limits of the [license agreement](https://underautomation.com/abb/eula).

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## API reference

**LicenseInfo** ([reference](../api/underautomation.abb.license.md#licenseinfo))

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

**LicenseState** ([reference](../api/underautomation.abb.license.md#licensestate))

- None_: No license has been provided
- Invalid: The pair License Identifier and License Key are incompatible, you cannot use the library
- Trial: The library is in a trial period, you can use the library
- ExtraTrial: The library is in an extra trial period, you can use the library
- Expired: The trial period as expired, you no more can use the library
- MaintenanceNeeded: Your license does not allow you to use such a recent release. Please buy maintenance to use this version
- Licensed: Congratulations, the library is licensed.

**InvalidLicenseException** ([reference](../api/underautomation.abb.license.md#invalidlicenseexception))

- `LicenseInfo: LicenseInfo (read only)`: The license that causes this exception
- Inherited from System.Exception: `Message`, `InnerException`
