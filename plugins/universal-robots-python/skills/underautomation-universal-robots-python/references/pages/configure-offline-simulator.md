# Develop without a robot (URSim)

Install URSim, the simulator of Universal Robots, in VirtualBox for PolyScope 5 or in Docker for PolyScope X, and connect the SDK to it.

Web page: https://underautomation.com/universal-robots/documentation/configure-offline-simulator

This page shows how to develop and test an application without a robot, with URSim, the simulator of Universal Robots. URSim runs the software of the controller: the SDK connects to it like to a real robot.

## Which simulator

| Simulator        | Robots                     | Runs in                               | Interfaces for the SDK                                                  |
| ---------------- | -------------------------- | ------------------------------------- | ----------------------------------------------------------------------- |
| URSim PolyScope  | CB-Series and e-Series     | A Linux virtual machine (VirtualBox)  | All: Primary Interface, Dashboard, RTDE, Interpreter Mode, SSH and SFTP |
| URSim PolyScope X | Robots with PolyScope X   | A Docker container                    | REST API, Primary Interface, RTDE                                       |

Download URSim from the [download center of Universal Robots](https://www.universal-robots.com/download/), in the `Software` section of your robot. A free account is needed.

## URSim PolyScope, in a virtual machine

### Install

1. Download and install [VirtualBox](https://www.virtualbox.org/wiki/Downloads). In the installer, keep the network features, including the host-only network.
2. Import the URSim virtual machine in VirtualBox.
3. Before you start it, open the settings of the virtual machine, `Network`. Attach the adapter to `Host-only Adapter`, with the default VirtualBox host-only adapter.

![VirtualBox network settings](https://underautomation.com/universal-robots/virtualbox-network-settings.png)

### Start a robot

1. Start the virtual machine. The Linux desktop shows one shortcut per robot model (UR3, UR5, UR10...).
2. Start the model you want. PolyScope opens.
3. Click the menu at the top right of PolyScope to see the address of the simulated robot. Use this address in `Connect`.

### Differences with a robot

- The Linux user is `ur`, password `easybot`. On a robot, it is `root`.
- The programs are in `/home/ur/ursim-current/programs`, instead of `/programs` on a robot.
- The services and the remote control are set in PolyScope, as on a robot: see [Prepare the robot](connect.md#prepare_the_robot).

## URSim PolyScope X, in Docker

### Install

1. Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/), then start it.
2. In a terminal, run the image of [URSim PolyScope X](https://hub.docker.com/r/universalrobots/ursim_polyscopex):

```bash
docker run --rm -it -p 80:80 -p 30001:30001 -p 30004:30004 --add-host "host.docker.internal:host-gateway" --env HOST_ARCH=amd64 --network bridge --privileged universalrobots/ursim_polyscopex:latest
```

| Option            | Role                                                                                      |
| ----------------- | ----------------------------------------------------------------------------------------- |
| `-p 80:80`        | The web interface and the REST API. If port 80 is used, write `-p 8080:80`                |
| `-p 30001:30001`  | The Primary Interface                                                                     |
| `-p 30004:30004`  | RTDE                                                                                      |
| `--privileged`    | The rights that the simulation needs                                                      |

### Connect

Open [http://localhost](http://localhost) in a browser (or `http://localhost:8080`) to see PolyScope X. Connect the SDK to `127.0.0.1`. With `-p 8080:80`, set `Rest.Port` to `8080` in `ConnectParameters`.

To accept commands, switch PolyScope X to remote control. The default password is `operator`.

![Remote control on PolyScope X](https://underautomation.com/universal-robots/switch-remote-polyscopex.png)

## Try it in the demo application

The demo application connects to URSim like to a robot.

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## What to read next

- [Connect to the robot](connect.md): the interfaces and their settings.
- [REST API](rest-api.md): the commands of PolyScope X.
- [Demo application](demo-app.md): try every interface without code.
