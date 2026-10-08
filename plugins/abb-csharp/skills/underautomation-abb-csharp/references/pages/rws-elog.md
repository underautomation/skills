# Event log

Read the controller event log, filter by domain and language, get the arguments of a message, and clear the log.

Web page: https://underautomation.com/abb/documentation/rws-elog

`robot.Rws.Elog` reads the event log of the controller, the same list of events the operator sees on the teach pendant. It is the first place to look when the robot stopped and you do not know why.

The log is split in domains. Each domain keeps its own messages, in a buffer of a fixed size, and the oldest message is dropped when the buffer is full.

## Domains

`GetDomains` lists the domains of the controller with the number of messages each one holds. The number of a domain is what every other method of the service takes as its first argument.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class ElogDomains
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Pass a language to get the names of the domains
        ElogDomain[] domains = robot.Rws.Elog.GetDomains("en");

        foreach (ElogDomain item in domains)
        {
            Console.WriteLine($"{item.Number} {item.Name}: {item.MessageCount}/{item.BufferSize}");
        }

        // The counters of one domain, without its name
        ElogDomain domain = robot.Rws.Elog.GetDomain(1);
        Console.WriteLine(domain.MessageCount);
        Console.WriteLine(domain.BufferSize);

        robot.Disconnect();
    }
}
```

Pass a language code to get the names of the domains, for example `Common`, `Operational` or `Safety`. Without a language the names are null and only the numbers and the counters are read, which is faster. The common domain is always there, the other ones depend on the options installed on the controller.

`GetDomain` reads the counters of one domain. The controller does not report the name there, read it from `GetDomains`.

## Read messages

`GetMessages` returns the messages of one domain. The SDK reads the pages of the answer for you and returns one array, so a domain holding hundreds of messages is read in one call.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class ElogMessages
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // The 20 most recent messages of the domain 1, with their full text in English
        ElogMessage[] messages = robot.Rws.Elog.GetMessages(1, ElogMessageOrder.NewestFirst, "en", 20);

        foreach (ElogMessage message in messages)
        {
            Console.WriteLine($"{message.Timestamp:yyyy-MM-dd HH:mm:ss} [{message.Type}] {message.Code} {message.Title}");
        }

        // Titles only, much faster on a domain holding hundreds of messages
        ElogMessage[] titles = robot.Rws.Elog.GetMessageTitles(1, "en", ElogMessageOrder.NewestFirst, 50);

        // The oldest messages first, without any text, so no language is needed
        ElogMessage[] oldest = robot.Rws.Elog.GetMessages(1, ElogMessageOrder.OldestFirst, null, 10);

        foreach (ElogMessage message in oldest)
        {
            Console.WriteLine($"{message.SequenceNumber} {message.Code} {message.Type} {message.SourceName}");
        }

        robot.Disconnect();
    }
}
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

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class ElogOneMessage
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // One message of a domain, from its sequence number
        ElogMessage message = robot.Rws.Elog.GetMessage(1, 42, "en");

        Console.WriteLine(message.Title);
        Console.WriteLine(message.Description);
        Console.WriteLine(message.Consequences);
        Console.WriteLine(message.Causes);
        Console.WriteLine(message.Actions);

        // The values the controller substitutes into the text of the message
        foreach (ElogMessageArgument argument in message.Arguments)
        {
            Console.WriteLine($"{argument.Index}: {argument.Value} ({argument.Type})");
        }

        // OmniCore only: the same message, without naming the domain it belongs to
        ElogMessage direct = robot.Rws.Elog.GetMessageBySequenceNumber(42, "en");

        robot.Disconnect();
    }
}
```

The arguments are the values the controller substitutes into the text of the message, for example the name of the task that was started. Each one carries its position in the message, its type as reported by the controller and its value as text.

`GetMessageBySequenceNumber` reads a message without naming its domain. Only an OmniCore exposes it. On an IRC5 the SDK throws an `RwsException` that says to use `GetMessage` with the domain instead.

## Clear and export the log

`ClearMessages` empties one domain, `ClearAllMessages` empties them all. The messages are gone for good, the controller keeps no copy of what it cleared. `ClearAllMessages` leaves the internal domain the controller reserves for itself untouched.

```csharp
using UnderAutomation.ABB;

public class ElogClear
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Delete every message of one domain
        robot.Rws.Elog.ClearMessages(1);

        // Delete every message of every domain
        robot.Rws.Elog.ClearAllMessages();

        // Ask the controller to write the whole event log to one file of its own file system.
        // The call returns before the file is complete.
        robot.Rws.Elog.SaveInSystemDumpFormat("$temp/elog.txt");

        // Read the result back with the file service
        string dump = robot.Rws.File.GetFileAsText("$temp/elog.txt");

        robot.Disconnect();
    }
}
```

`SaveInSystemDumpFormat` asks the controller to write the whole event log to one file of its own file system. This is the format ABB support asks for. The controller accepts the request and writes the file afterwards, so the call returns before the file is complete. Read the destination with the [file system service](rws-files.md) to know when it is there, and to bring it back on your PC.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## API reference

**Methods of ElogService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#elogservice-robotrwselog))

- `void ClearAllMessages()`: Deletes every message of every event log domain (synchronous)
  - async: `Task ClearAllMessagesAsync(CancellationToken cancellationToken = default)`
- `void ClearMessages(int domain)`: Deletes every message of one event log domain (synchronous)
  - async: `Task ClearMessagesAsync(int domain, CancellationToken cancellationToken = default)`
- `ElogDomain GetDomain(int domain)`: Gets the number of messages one event log domain holds and the number it can hold (synchronous)
  - async: `Task<ElogDomain> GetDomainAsync(int domain, CancellationToken cancellationToken = default)`
- `ElogDomain[] GetDomains(string language = null)`: Gets every event log domain of the controller, with the number of messages each one holds (synchronous)
  - async: `Task<ElogDomain[]> GetDomainsAsync(string language = null, CancellationToken cancellationToken = default)`
- `ElogMessage GetMessage(int domain, int sequenceNumber, string language = null)`: Gets one message of an event log domain (synchronous)
  - async: `Task<ElogMessage> GetMessageAsync(int domain, int sequenceNumber, string language = null, CancellationToken cancellationToken = default)`
- `ElogMessage GetMessageBySequenceNumber(int sequenceNumber, string language = null)`: Gets one message from its sequence number alone, without naming the domain it belongs to (synchronous)
  - async: `Task<ElogMessage> GetMessageBySequenceNumberAsync(int sequenceNumber, string language = null, CancellationToken cancellationToken = default)`
- `ElogMessage[] GetMessageTitles(int domain, string language, ElogMessageOrder order = ElogMessageOrder.NewestFirst, int? maxCount = null)`: Gets the messages held by one event log domain, with their short text only (synchronous)
  - async: `Task<ElogMessage[]> GetMessageTitlesAsync(int domain, string language, ElogMessageOrder order = ElogMessageOrder.NewestFirst, int? maxCount = null, CancellationToken cancellationToken = default)`
- `ElogMessage[] GetMessages(int domain, ElogMessageOrder order = ElogMessageOrder.NewestFirst, string language = null, int? maxCount = null)`: Gets the messages held by one event log domain (synchronous)
  - async: `Task<ElogMessage[]> GetMessagesAsync(int domain, ElogMessageOrder order = ElogMessageOrder.NewestFirst, string language = null, int? maxCount = null, CancellationToken cancellationToken = default)`
- `void SaveInSystemDumpFormat(string path)`: Asks the controller to write the whole event log to one file on its own file system (synchronous)
  - async: `Task SaveInSystemDumpFormatAsync(string path, CancellationToken cancellationToken = default)`

**ElogDomain** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#elogdomain))

- `ElogDomain()`: Initializes a new instance of the Data.ElogDomain class
- `int? BufferSize { get; set; }`: Number of messages the domain can hold before the oldest ones are discarded, null when the controller did not report it
- `int? MessageCount { get; set; }`: Number of messages currently held by the domain, null when the controller did not report it
- `string Name { get; set; }`: Name of the domain, for example "Operational" or "Safety". Only filled when a language was asked for, null otherwise.
- `int Number { get; set; }`: Number identifying the domain, which is the value to pass to the methods reading its messages

**ElogMessage** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#elogmessage))

- `ElogMessage()`: Initializes a new instance of the Data.ElogMessage class
- `string Actions { get; set; }`: Text describing the recommended actions. Only filled when a language was asked for.
- `int ArgumentCount { get; }`: Number of arguments of the message
- `ElogMessageArgument[] Arguments { get; set; }`: Values the controller substitutes into the text of the message
- `string Causes { get; set; }`: Text describing the probable causes of the event. Only filled when a language was asked for.
- `int? Code { get; set; }`: Number identifying the kind of event, the one printed on the teach pendant
- `string Consequences { get; set; }`: Text describing what the event implies for the robot. Only filled when a language was asked for.
- `string Description { get; set; }`: Long text describing what happened. Only filled when a language was asked for.
- `int? DomainNumber { get; set; }`: Number of the domain the message belongs to, null when the controller did not report it
- `int? SequenceNumber { get; set; }`: Number identifying the message inside its domain. Messages are numbered in the order they were logged, so a higher number is a more recent message.
- `string SourceName { get; set; }`: Part of the controller that logged the message, for example "MC0"
- `DateTime? Timestamp { get; set; }`: Moment the event was logged, null when the controller did not report it
- `string Title { get; set; }`: Short text of the message. Only filled when a language was asked for.
- `ElogMessageType Type { get; set; }`: Severity of the message

**ElogMessageArgument** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#elogmessageargument))

- `ElogMessageArgument()`: Initializes a new instance of the Data.ElogMessageArgument class
- `int Index { get; set; }`: Position of the argument in the message, starting at 1
- `string Type { get; set; }`: Type of the argument reported by the controller, for example "string", "long" or "float"
- `string Value { get; set; }`: Value of the argument, always as text

**ElogMessageType** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#elogmessagetype))

- Error: Error event
- Information: State change, or informational event
- Unknown: The message type could not be determined
- Warning: Warning event

**ElogMessageOrder** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#elogmessageorder))

- NewestFirst: Most recent message first
- OldestFirst: Oldest message first
