# Event log

Read the controller event log, filter by domain and language, get the arguments of a message, and clear the log.

Web page: https://underautomation.com/abb/documentation/rws-elog

`robot.Rws.Elog` reads the event log of the controller, the same list of events the operator sees on the teach pendant. It is the first place to look when the robot stopped and you do not know why.

The log is split in domains. Each domain keeps its own messages, in a buffer of a fixed size, and the oldest message is dropped when the buffer is full.

## Domains

`GetDomains` lists the domains of the controller with the number of messages each one holds. The number of a domain is what every other method of the service takes as its first argument.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# Pass a language to get the names of the domains
domains = robot.rws.elog.get_domains("en")

for item in domains:
    print(f"{item.number} {item.name}: {item.message_count}/{item.buffer_size}")

# The counters of one domain, without its name
domain = robot.rws.elog.get_domain(1)
print(domain.message_count)
print(domain.buffer_size)

robot.disconnect()
```

Pass a language code to get the names of the domains, for example `Common`, `Operational` or `Safety`. Without a language the names are null and only the numbers and the counters are read, which is faster. The common domain is always there, the other ones depend on the options installed on the controller.

`GetDomain` reads the counters of one domain. The controller does not report the name there, read it from `GetDomains`.

## Read messages

`GetMessages` returns the messages of one domain. The SDK reads the pages of the answer for you and returns one array, so a domain holding hundreds of messages is read in one call.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.elog_message_order import ElogMessageOrder

robot = AbbController()
robot.connect("192.168.0.1")

# The 20 most recent messages of the domain 1, with their full text in English
messages = robot.rws.elog.get_messages(1, ElogMessageOrder.NewestFirst, "en", 20)

for message in messages:
    print(f"{message.timestamp} [{message.type}] {message.code} {message.title}")

# Titles only, much faster on a domain holding hundreds of messages
titles = robot.rws.elog.get_message_titles(1, "en", ElogMessageOrder.NewestFirst, 50)

# The oldest messages first, without any text, so no language is needed
oldest = robot.rws.elog.get_messages(1, ElogMessageOrder.OldestFirst, None, 10)

for message in oldest:
    print(f"{message.sequence_number} {message.code} {message.type} {message.source_name}")

robot.disconnect()
```

| Argument   | Effect                                                               |
| ---------- | -------------------------------------------------------------------- |
| `domain`   | Number of the domain, from `GetDomains`                              |
| `order`    | `NewestFirst` or `OldestFirst`                                       |
| `language` | Two letter code of the language of the texts, null to skip the texts |
| `maxCount` | Stops the reading early, which is what a "latest events" view needs  |

Leave `language` null when you only need the code, the severity and the timestamp of each event. The controller then sends much less text, and the texts of `ElogMessage` stay null.

`GetMessageTitles` is the middle ground: it returns the short text of each message and leaves out the long texts and the arguments. On a busy domain it is a lot faster than `GetMessages`.

| `ElogMessageType` | Meaning                                                      |
| ----------------- | ------------------------------------------------------------ |
| `Information`     | State change or informational event                          |
| `Warning`         | Warning event                                                |
| `Error`           | Error event                                                  |
| `Unknown`         | The controller reports a severity this library does not know |

`Code` is the number printed on the teach pendant for that kind of event. `SequenceNumber` identifies the message inside its domain, and the messages are numbered in the order they were logged, so a higher number is a more recent message.

## Read one message

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes. Reading a message from its sequence number alone needs an OmniCore controller

`GetMessage` returns one message with everything the controller knows about it: the long description, the consequences for the robot, the probable causes, the actions to take, and the arguments.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# One message of a domain, from its sequence number
message = robot.rws.elog.get_message(1, 42, "en")

print(message.title)
print(message.description)
print(message.consequences)
print(message.causes)
print(message.actions)

# The values the controller substitutes into the text of the message
for argument in message.arguments:
    print(f"{argument.index}: {argument.value} ({argument.type})")

# OmniCore only: the same message, without naming the domain it belongs to
direct = robot.rws.elog.get_message_by_sequence_number(42, "en")

robot.disconnect()
```

The arguments are the values the controller substitutes into the text of the message, for example the name of the task that was started. Each one carries its position in the message, its type as reported by the controller and its value as text.

`GetMessageBySequenceNumber` reads a message without naming its domain. Only an OmniCore exposes it. On an IRC5 the SDK throws an `RwsException` that says to use `GetMessage` with the domain instead.

## Clear and export the log

`ClearMessages` empties one domain, `ClearAllMessages` empties them all. The messages are gone for good, the controller keeps no copy of what it cleared. `ClearAllMessages` leaves the internal domain the controller reserves for itself untouched.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# Delete every message of one domain
robot.rws.elog.clear_messages(1)

# Delete every message of every domain
robot.rws.elog.clear_all_messages()

# Ask the controller to write the whole event log to one file of its own file system.
# The call returns before the file is complete.
robot.rws.elog.save_in_system_dump_format("$temp/elog.txt")

# Read the result back with the file service
dump = bytes(robot.rws.file.get_file_as_bytes("$temp/elog.txt")).decode("utf-8")

robot.disconnect()
```

`SaveInSystemDumpFormat` asks the controller to write the whole event log to one file of its own file system. This is the format ABB support asks for. The controller accepts the request and writes the file afterwards, so the call returns before the file is complete. Read the destination with the [file system service](rws-files.md) to know when it is there, and to bring it back on your PC.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## API reference

**Methods of ElogService** ([reference](../api/underautomation.abb.rws.services.md#elogservice-robotrwselog))

- `get_domains(language: str=None) -> typing.List[ElogDomain]`: Gets every event log domain of the controller, with the number of messages each one holds (synchronous)
- `get_domain(domain: int) -> ElogDomain`: Gets the number of messages one event log domain holds and the number it can hold (synchronous)
- `get_messages(domain: int, order: ElogMessageOrder=ElogMessageOrder.NewestFirst, language: str=None, maxCount: int | None=None) -> typing.List[ElogMessage]`: Gets the messages held by one event log domain (synchronous)
- `get_message_titles(domain: int, language: str, order: ElogMessageOrder=ElogMessageOrder.NewestFirst, maxCount: int | None=None) -> typing.List[ElogMessage]`: Gets the messages held by one event log domain, with their short text only (synchronous)
- `get_message(domain: int, sequenceNumber: int, language: str=None) -> ElogMessage`: Gets one message of an event log domain (synchronous)
- `get_message_by_sequence_number(sequenceNumber: int, language: str=None) -> ElogMessage`: Gets one message from its sequence number alone, without naming the domain it belongs to (synchronous)
- `clear_messages(domain: int) -> None`: Deletes every message of one event log domain (synchronous)
- `clear_all_messages() -> None`: Deletes every message of every event log domain (synchronous)
- `save_in_system_dump_format(path: str) -> None`: Asks the controller to write the whole event log to one file on its own file system (synchronous)

**ElogDomain** ([reference](../api/underautomation.abb.rws.data.md#elogdomain))

- `ElogDomain()`: Initializes a new instance of the ElogDomain class
- `number: int`: Number identifying the domain, which is the value to pass to the methods reading its messages
- `name: str`: Name of the domain, for example "Operational" or "Safety". Only filled when a language was asked for, null otherwise.
- `message_count: int | None`: Number of messages currently held by the domain, null when the controller did not report it
- `buffer_size: int | None`: Number of messages the domain can hold before the oldest ones are discarded, null when the controller did not report it

**ElogMessage** ([reference](../api/underautomation.abb.rws.data.md#elogmessage))

- `ElogMessage()`: Initializes a new instance of the ElogMessage class
- `domain_number: int | None`: Number of the domain the message belongs to, null when the controller did not report it
- `sequence_number: int | None`: Number identifying the message inside its domain. Messages are numbered in the order they were logged, so a higher number is a more recent message.
- `type: ElogMessageType`: Severity of the message
- `code: int | None`: Number identifying the kind of event, the one printed on the teach pendant
- `source_name: str`: Part of the controller that logged the message, for example "MC0"
- `timestamp: datetime | None`: Moment the event was logged, null when the controller did not report it
- `title: str`: Short text of the message. Only filled when a language was asked for.
- `description: str`: Long text describing what happened. Only filled when a language was asked for.
- `consequences: str`: Text describing what the event implies for the robot. Only filled when a language was asked for.
- `causes: str`: Text describing the probable causes of the event. Only filled when a language was asked for.
- `actions: str`: Text describing the recommended actions. Only filled when a language was asked for.
- `arguments: typing.List[ElogMessageArgument]`: Values the controller substitutes into the text of the message
- `argument_count: int (read only)`: Number of arguments of the message

**ElogMessageArgument** ([reference](../api/underautomation.abb.rws.data.md#elogmessageargument))

- `ElogMessageArgument()`: Initializes a new instance of the ElogMessageArgument class
- `index: int`: Position of the argument in the message, starting at 1
- `type: str`: Type of the argument reported by the controller, for example "string", "long" or "float"
- `value: str`: Value of the argument, always as text

**ElogMessageType** ([reference](../api/underautomation.abb.rws.data.md#elogmessagetype))

- Unknown: The message type could not be determined
- Information: State change, or informational event
- Warning: Warning event
- Error: Error event

**ElogMessageOrder** ([reference](../api/underautomation.abb.rws.data.md#elogmessageorder))

- NewestFirst: Most recent message first
- OldestFirst: Oldest message first
