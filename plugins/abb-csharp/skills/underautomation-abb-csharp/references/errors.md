# Errors of the ABB SDK (C#)

SDK version 1.1.0. The exceptions of the SDK, and the pages that describe when they are thrown. The message of an exception says what failed: read it first, then the page of the feature.

## InvalidLicenseException

`class InvalidLicenseException : Exception, ISerializable`

Exception thrown while using the product if the license is not valid.

Reference: [UnderAutomation.ABB.License](api/UnderAutomation.ABB.License.md#invalidlicenseexception)

Pages that describe it: [license](pages/license.md).

## RwsException

`class RwsException : Exception, ISerializable`

Exception thrown when an RWS API request fails. Compatible with RWS v1 and v2.

Reference: [UnderAutomation.ABB.Rws](api/UnderAutomation.ABB.Rws.md#rwsexception)

Pages that describe it: [connect](pages/connect.md), [virtual-controller](pages/virtual-controller.md), [rws](pages/rws.md), [rws-controller](pages/rws-controller.md), [rws-panel](pages/rws-panel.md), [rws-rapid-symbols](pages/rws-rapid-symbols.md), [rws-io](pages/rws-io.md), [rws-motion](pages/rws-motion.md), [rws-files](pages/rws-files.md), [rws-elog](pages/rws-elog.md), [rws-mastership](pages/rws-mastership.md), [irc5-vs-omnicore](pages/irc5-vs-omnicore.md), [read-write-io-signals](pages/read-write-io-signals.md).
