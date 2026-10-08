# Licensing

The 30 day trial, the license key and RegisterLicense, the license states, the maintenance and the source license of the Fanuc SDK.

Web page: https://underautomation.com/fanuc/documentation/license

This page explains the licensing of the Fanuc SDK: the 30 day trial, the license key, the license states and the maintenance. The SDK is a commercial product. Every feature is available during the trial.

## Trial period

The trial starts the first time the library is used on a machine and lasts 30 days. Nothing has to be registered, and no feature is disabled during the trial.

`FanucRobot.LicenseInfo` gives the current state. `EvaluationDaysLeft` is the number of days left, and becomes negative when the trial has expired.

## Register a license

### RegisterLicense

Buy a license ([see pricing](https://underautomation.com/order)): you receive a license key and the name of your organization (the licensee). Pass both to the static method `RegisterLicense` of `FanucRobot`, once, before the first connection.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.License;

public class License
{
    static void Main()
    {
        // Register the license once, before the first connection
        FanucRobot.RegisterLicense("YourCompanyName", "YOUR_LICENSE_KEY");

        LicenseInfo info = FanucRobot.LicenseInfo;

        // Number of trial days remaining
        int? evaluationDaysLeft = info.EvaluationDaysLeft;

        bool licenseValid = info.State == LicenseState.Licensed;

        // A readable description of the current state
        Console.WriteLine(info);

        // Check the license once at startup, rather than catching the exception
        // on every connection
        if (!FanucRobot.LicenseInfo.IsLicensed)
        {
            Console.WriteLine(FanucRobot.LicenseInfo);
            return;
        }
    }
}
```

The registration is static: it applies to the whole application, not to one `FanucRobot`. You can register a key after the end of the trial.

`LicenseInfo.ToString()` gives a readable description of the state. It is the message of an `InvalidLicenseException`.

### License states

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

The offline features (kinematics, motion planner, file parsers) do not connect to a controller.

## Source license

The Standard and Pro licenses deliver the obfuscated DLL. The Source license also delivers the full C# code of the library and its Visual Studio solution, to change and build it yourself, within the limits of the [license agreement](https://underautomation.com/fanuc/eula).

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**LicenseInfo** ([reference](../api/UnderAutomation.Fanuc.License.md#licenseinfo))

- `LicenseInfo(string licenseIdentifier, string licenseKey)`: Create a new LicenseInfo instance to retrieve informations about a pair of identifier/key This class should not be used to register your product. Please use static function RegisterLicense to specify your license.
- `int? EvaluationDaysLeft { get; }`: Remaining days of the trial period. Null if the product is licensed. It could be negative if the trial period is ended since several days.
- `DateTime EvaluationStartDate { get; }`: The date the trial period starts. If the product is licensed, the date of the library first use.
- `bool IsLicensed { get; }`: True if the license state is Licensed, Trial or ExtraTrial ; false otherwise
- `DateTime? LicenseIssuedDate { get; }`: The date you get the license
- `string LicenseKey { get; }`: The license key supplied by UnderAutomation (null for trial period)
- `string Licensee { get; }`: Name of your organisation
- `DateTime? MaintenanceExpirationDate { get; }`: The date your maintenance contract end and you no longer can use this license with newer versions.
- `int MaintenanceYears { get; }`: Number of maintenance years included in your license
- `string Product { get; }`: Commercial name of this .NET Software library
- `DateTime ProductReleaseDate { get; }`: The date this version of the product was released.
- `LicenseState State { get; }`: The current license state
- `DateTime? TrialPeriodExpirationDate { get; }`: The date the product will expire. Null if the product is licensed.

**LicenseState** ([reference](../api/UnderAutomation.Fanuc.License.md#licensestate))

- Expired: The trial period as expired, you no more can use the library
- ExtraTrial: The library is in an extra trial period, you can use the library
- Invalid: The pair License Identifier and License Key are incompatible, you cannot use the library
- Licensed: Congratulations, the library is licensed.
- MaintenanceNeeded: Your license does not allow you to use such a recent release. Please buy maintenance to use this version
- None: No license has been provided
- Trial: The library is in a trial period, you can use the library

**InvalidLicenseException** ([reference](../api/UnderAutomation.Fanuc.License.md#invalidlicenseexception))

- `LicenseInfo LicenseInfo { get; }`: The license that causes this exception
