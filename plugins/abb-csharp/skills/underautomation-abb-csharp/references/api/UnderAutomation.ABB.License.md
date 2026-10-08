# UnderAutomation.ABB.License

## InvalidLicenseException

`class InvalidLicenseException : Exception, ISerializable`

Exception thrown while using the product if the license is not valid.

- `LicenseInfo LicenseInfo { get; }`: The license that causes this exception

## LicenseInfo

`sealed class LicenseInfo`

Information about a license key

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

## LicenseState

`enum LicenseState`

States that can take a license

- Expired: The trial period as expired, you no more can use the library
- ExtraTrial: The library is in an extra trial period, you can use the library
- Invalid: The pair License Identifier and License Key are incompatible, you cannot use the library
- Licensed: Congratulations, the library is licensed.
- MaintenanceNeeded: Your license does not allow you to use such a recent release. Please buy maintenance to use this version
- None: No license has been provided
- Trial: The library is in a trial period, you can use the library
