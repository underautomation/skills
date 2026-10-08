# Enable Telnet on your robot

TELNET is natively available on ROBOGUIDE and all Fanuc robots without any option. Learn how to enable it step by step.

Web page: https://underautomation.com/fanuc/documentation/telnet-enable-on-robot

> **Telnet KCL is a legacy protocol.** It is not secured: the password and the commands are sent in clear text. It is hard to maintain: the answers of the controller change with the firmware version, and ROBOGUIDE behaves differently from a real controller. The KCL commands of `robot.Telnet` are also available with `robot.Cgtp.Kcl`, through the web server of the controller (firmware V8.30 and later), without Telnet setup. Prefer it for new developments: see [KCL commands over CGTP](cgtp-kcl.md).

Telnet KCL allows you to send commands to a Fanuc robot, such as resetting alarms, writing variables, setting an IO, and more. This feature is natively available on all Fanuc robots without requiring any additional options.

To enable a TELNET connection on your real or simulated ROBOGUIDE robot, please follow the instructions below. On a real robot, the connection is established via TCP on port 23. In ROBOGUIDE, while this port is open, it only allows read-only access. Therefore, to enable full bidirectional communication via Telnet, you must follow the provided instructions to set up a dedicated alternative port.

This library allows you to send KCL (Karel Command Language) commands over the TELNET connection.

## 1. Set a TELNET password

Adding a password is mandatory to enable telnet control of the robot.

- Press `MENU` on the robot's teach pendant.

![Menu button](https://underautomation.com/fanuc/documentation/menu.png)

- Select `SETUP` / `-- NEXT --` / `Host Comm`

![Host Comm](https://underautomation.com/fanuc/documentation/host-comm.png)

- Select `TELNET` and press `DETAIL`

![Setup Protocols TELNET](https://underautomation.com/fanuc/documentation/setup-protocols-telnet.png)

- Add a password to the KCL feature

![TELNET Password](https://underautomation.com/fanuc/documentation/telnet-password.png)

- Press `ENTER` and `PREV` on the robot's teach pendant to validate this password.

- Cold start your robot

## 2. If you have option J541 (Password Protection)

If the menu `SETUP` / `Passwords` exists on your robot, you have option "Password Protection" J541. You must then authorize the TELNET connection by modifying its security level.

- Press `MENU` on the robot's teach pendant.

![Menu button](https://underautomation.com/fanuc/documentation/menu.png)

- Select `SETUP` / `Passwords`

- Login as `INSTALL`

![Passwords](https://underautomation.com/fanuc/documentation/passwords.png)

- Download this file : <a href="https://underautomation.com/fanuc/documentation/PASSWORD.xml" download>PASSWORD.xml</a>,

On a real robot, transfer this file on a USB key and plug it into the pendant USB port.

On ROBOGUIDE, put this file into the `UT1` directory.

```xml
<?xml version="1.0"?>
<PASSWORD>
  <PWD level="0" const="1" access="1"/>
</PASSWORD>
```

- Set import device to UT1 : press `MENU` key / `File` / `File` / `[CONFIG]` / `Set Device` / `--next page--` / `USB on TP (UT1:)`

- press `MENU` key / `SETUP` / `Passwords` / `>` at the bottom right of the pendant screen

![Setup password](https://underautomation.com/fanuc/documentation/setup-passwords.png)

- Select `CONFIG` and import `PASSWORD.xml`

![Set TELNET access](https://underautomation.com/fanuc/documentation/set-telnet-access.gif)

- Cold start your robot

## 3. Special configuration for ROBOGUIDE

If you are using ROBOGUIDE, you must also enable the KCL feature, as the default TELNET connection on port TCP 23 is read-only.

Currently, Telnet KCL simulation is not supported in ROBOGUIDE v10, only up to v9.

- Start ROBOGUIDE, open a cell and show the teach pendant ![teach pendant](https://underautomation.com/fanuc/documentation/show-teach.png)

- press `MENU` key / `SETUP` / `Port Init`

![SETUP Port Init](https://underautomation.com/fanuc/documentation/setup-port-init.png)

- Select `DETAIL` on first connector

![SETUP Port Init Connectors](https://underautomation.com/fanuc/documentation/setup-port-init-connectors.png)

- Set `Device` to `KCL/CRT`, then press button `PREV` on teach pendant

![SETUP Port Init Detail](https://underautomation.com/fanuc/documentation/setup-port-init-detail.png)

- Cold start your robot

- You can then see KCL commands in the KCL window : `Robot` menu / `KCL Window`

![KCL Window](https://underautomation.com/fanuc/documentation/kcl-window.png)
