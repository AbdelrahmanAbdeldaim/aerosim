# Dev Container

A VS Code dev container with ROS 2 Jazzy, the colcon toolchain, and the Micro
XRCE-DDS Agent already built, so the workspace needs no host ROS installation.

Isaac Sim, Pegasus Simulator, and PX4 SITL stay on the **host** — Isaac Sim is
installed natively (see the [simulation setup guide](../../simulation/README.md)).
The container runs with host networking, so ROS 2 nodes inside it talk to the
host PX4 instance as if they were running natively.

## Prerequisites

* Docker Engine with the Compose plugin.
* The [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
  extension for VS Code.
* Optional: the NVIDIA Container Toolkit, for GPU-accelerated RViz. Without a
  GPU, delete the `deploy:` block from `docker-compose.yml`.

## Opening the Container

Open **`drone_ws`** in VS Code — not the repository root, since Dev Containers
only looks for `.devcontainer/` in the folder you opened — then run
**Dev Containers: Reopen in Container** from the command palette. The first
build takes several minutes; later starts are instant.

`drone_ws` keeps its name inside the container: it mounts at `/drone_ws`, which
is both the working directory and the folder VS Code opens, so `colcon build`
works straight out of a fresh terminal.

Nothing else from the repository is mounted. One practical consequence: `git`
does not work inside the container, because `.git` lives at the repository root,
one level above the mount. Run git on the host.

## GUI Applications

RViz and rqt render through the host X server via the mounted
`/tmp/.X11-unix` socket. If a GUI fails to open with an authorization error,
allow local container clients on the host:

```bash
xhost +local:docker
```
