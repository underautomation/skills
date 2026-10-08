# underautomation.staubli.license

## InvalidLicenseException

`from UnderAutomation.Staubli.License import InvalidLicenseException`

Exception thrown while using the product if the license is not valid.

The SDK raises this .NET type: catch it with `except InvalidLicenseException as e` after the import above. Its members keep their .NET names. The class `InvalidLicenseException` of the module `underautomation.staubli.license.invalid_license_exception` is not a Python exception and cannot be caught.

- `LicenseInfo: LicenseInfo (read only)`: The license that causes this exception
- Inherited from System.Exception: `Message`, `InnerException`

## LicenseInfo

`from underautomation.staubli.license.license_info import LicenseInfo`

Information about a license key

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

## LicenseState

`from underautomation.staubli.license.license_state import LicenseState`

States that can take a license

- None_: No license has been provided
- Invalid: The pair License Identifier and License Key are incompatible, you cannot use the library
- Trial: The library is in a trial period, you can use the library
- ExtraTrial: The library is in an extra trial period, you can use the library
- Expired: The trial period as expired, you no more can use the library
- MaintenanceNeeded: Your license does not allow you to use such a recent release. Please buy maintenance to use this version
- Licensed: Congratulations, the library is licensed.
