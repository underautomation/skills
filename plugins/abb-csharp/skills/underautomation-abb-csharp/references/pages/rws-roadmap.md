# Roadmap: operations not wrapped yet

Robot Web Services offers more operations than the SDK wraps today. This page lists what is on the roadmap, and how to have an operation prioritized for your project.

Web page: https://underautomation.com/abb/documentation/rws-roadmap

Robot Web Services exposes more operations than the SDK wraps today. This page lists the ones that are not wrapped yet, grouped by area.

The current version covers 239 of the 353 operations of the Robot Web Services interface. The 114 operations below are known and documented, but no method of the SDK calls them yet.

**These functions are on the roadmap, not in the SDK today.** Their order of implementation follows customer demand. If you need one of them, [contact us](https://underautomation.com/contact) and we will schedule it. Wrapping an operation that already exists in Robot Web Services is usually fast, so a clear need on your side can move it forward quickly.

The list is built from the RWS 2.0 interface (OmniCore, RobotWare 7). Most of these operations also exist on RWS 1.0 (IRC5, RobotWare 6).

## Configuration database (CFG)

The CFG subsystem holds the controller configuration: I/O (EIO), motion (MOC), controller (SYS), process (PROC) and communication (SIO) domains. The SDK does not expose it yet.

- List the configuration domains, the types of a domain and the instances of a type.
- Read the attributes of a type and the values of an instance.
- Create, update and delete a configuration instance, and create an instance with its default values.
- Reset a domain or a set of instances to their default content.
- Load a configuration file into a domain, and save a domain to a file.
- Validate a change (add, update, delete) before it is applied.

## Users, roles and grants (UAS)

The User Authorization System stores the accounts, the roles and the grants of the controller. The SDK uses the UAS grant of the current session only through error handling. It does not manage the UAS content.

- List users, list roles, list all defined grants.
- Read a user (description, enabled state, roles, grants, password change policy) and a role (description, grants).
- Create and delete a user, create and delete a role.
- Edit a user description, enable or disable a user, change a password, allow or block password change.
- Add and remove roles on a user, add and remove grants on a role.

## User session and manual mode privileges (RMMP)

These operations act on the current HTTP user and on the Request Manual Mode Privileges mechanism, used to get write access while the controller is in manual mode.

- Read the login information and the registered state of the current user, check whether the current user holds a given grant.
- Register the current user, impersonate another user for the session.
- Request manual mode privileges, poll the request, cancel it, and grant or deny a request from another client.

## Event subscriptions (WebSocket)

Robot Web Services can push a notification when a resource changes, over a WebSocket, instead of the application polling. The SDK does not offer this yet, so state changes have to be polled today.

- Open a subscription group on a set of resources, for example an I/O signal, the controller state, the execution state, a RAPID variable or the event log.
- Edit the resources of an existing group.
- Close a group or remove single resources from it.
- Receive and decode the push messages of the WebSocket.

## Integrated Vision cameras

The Integrated Vision option connects cameras to the controller. The SDK does not expose the camera management.

- List the cameras, read a camera info, its status and its running job.
- Set a camera name, hostname, DNS, network configuration and user.
- Flash the camera LEDs, restart a camera, refresh the camera list.

## RAPID message queues (DIPC)

Data Inter-Process Communication is the Robot Web Services access to the RAPID message queues, used to exchange messages with a running RAPID program.

- List the queues, read the information of a queue.
- Create and delete a queue.
- Send a message to a queue and read a message from a queue.

## Safety configuration commands

The SDK reads the safety state, the safety mode and the safety violations. The commands that change the safety configuration are not wrapped.

- Unlock the safety configuration for editing.
- Add validation information and acknowledge a software synchronization.
- Reset the safety controller.

## Certificate store

The controller keeps a certificate store for secure connections.

- Read the store and the content of a certificate.
- Add a certificate, remove the certificates of a store.

## Device tree

Robot Web Services exposes the hardware device tree of the controller: drives, measurement boards, axis computers.

- Read the device tree.
- Search the device tree with a filter.

## Diagnostics and system installation

- Read the diagnostic data of the controller and save a diagnostic file.
- List the installed options.
- Read the installed system information, start a RobotWare system update and follow its status.
- Compress and decompress files on the controller.

## Network: advanced properties and Connected Services Gateway

The SDK reads and sets the standard network configuration. The following are not covered:

- Read the advanced network properties and check a route table entry.
- List and scan the cellular and Wi-Fi networks seen by the Connected Services Gateway.

## Teach pendant detach

- Start the detach sequence of the FlexPendant, cancel it, and read its status.

## RAPID service additions

The RAPID service is the largest one in the SDK. These operations are not wrapped yet:

- Deactivate one RAPID task or a set of RAPID tasks. Activation is already available.
- Read the motion pointer synchronization state of all tasks.
- Read a RAPID data object as a structured tree.
- Set the calibration of a single or dual arm robot.

## Control panel additions

- Read the enabling device required state.
- Set the virtual emergency stop, the enable switch and the keyless motors on state. These are mainly useful with a virtual controller.

## Event log by sequence number

- Read a single event log message by its global sequence number, across all domains.
