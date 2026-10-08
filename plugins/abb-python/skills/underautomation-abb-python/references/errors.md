# Errors of the ABB SDK (Python)

SDK version 1.1.0. The exceptions of the SDK, and the pages that describe when they are raised. The message of an exception says what failed: read it first, then the page of the feature.

The SDK raises the .NET exception. It is a Python exception: catch it with `except Exception as e` and read `str(e)`, or catch its .NET type, imported from its .NET namespace as shown below (the package loads the .NET library first).

Its members keep their .NET names: `e.Message`, `e.InnerException`. The classes of the same name in the `underautomation.abb` modules are not Python exceptions: `except` on one of them raises a `TypeError`. The reference of each exception lists its members.

## InvalidLicenseException

Exception thrown while using the product if the license is not valid.

Catch: `from UnderAutomation.ABB.License import InvalidLicenseException`, then `except InvalidLicenseException as e`.

Reference: [underautomation.abb.license](api/underautomation.abb.license.md#invalidlicenseexception)

Pages that describe it: [license](pages/license.md).

## RwsException

Exception thrown when an RWS API request fails. Compatible with RWS v1 and v2.

Catch: `from UnderAutomation.ABB.Rws import RwsException`, then `except RwsException as e`.

Reference: [underautomation.abb.rws](api/underautomation.abb.rws.md#rwsexception)

Pages that describe it: [get-started-python](pages/get-started-python.md), [connect](pages/connect.md), [virtual-controller](pages/virtual-controller.md), [rws](pages/rws.md), [rws-controller](pages/rws-controller.md), [rws-panel](pages/rws-panel.md), [rws-rapid-symbols](pages/rws-rapid-symbols.md), [rws-io](pages/rws-io.md), [rws-motion](pages/rws-motion.md), [rws-files](pages/rws-files.md), [rws-elog](pages/rws-elog.md), [rws-mastership](pages/rws-mastership.md), [irc5-vs-omnicore](pages/irc5-vs-omnicore.md), [read-write-io-signals](pages/read-write-io-signals.md).
