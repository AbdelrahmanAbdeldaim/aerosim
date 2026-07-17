# Drone Navstack Simulation

Isaac Sim scripts, USD stages, and reusable Python utilities for the Drone
Navstack project.

The Python distribution and import names are intentionally different:

| Purpose | Name |
| --- | --- |
| Package installed by `pip` | `drone-navstack-sim` |
| Package imported by Python | `drone_sim` |

## Prerequisites

1. [Install NVIDIA Isaac Sim 5.1](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/install_workstation.html) using NVIDIA's official workstation installation guide. Download and extract the Linux archive, run `./post_install.sh`, and verify the installation using `./isaac-sim.selector.sh`.
2. [Configure the environment variables](https://pegasussimulator.github.io/PegasusSimulator/source/setup/installation.html#configuring-the-environment-variables). Add `ISAACSIM_PATH`, `ISAACSIM_PYTHON`, `ISAACSIM`, and the `isaac_run` function to your shell configuration, then open a new terminal.
3. [Install Pegasus Simulator](https://pegasussimulator.github.io/PegasusSimulator/source/setup/installation.html#installing-the-pegasus-simulator). Clone Pegasus, register its `extensions/` directory in Isaac Sim, enable the extension, and install `pegasus.simulator` with Isaac Sim's Python interpreter.
4. Install PX4 Autopilot v1.17 for software-in-the-loop flight control using the instructions below, then configure Pegasus with the PX4 repository path.

Install the PX4 build dependencies and clone the v1.17 release:

```bash
sudo apt install git make cmake python3-pip
git clone https://github.com/PX4/PX4-Autopilot.git
cd PX4-Autopilot
git checkout v1.17.0
git submodule update --init --recursive
bash ./Tools/setup/ubuntu.sh
```

Restart the computer after the setup script finishes, then build PX4 SITL for
use with Pegasus:

```bash
cd ~/PX4-Autopilot
make px4_sitl_default none
```

If the repository was cloned somewhere else, use that path instead and set the
same PX4 path in the Pegasus configuration.

Pegasus documents Isaac Sim 5.1 on Ubuntu 22.04 as its tested setup. Check the
upstream compatibility notes before using a different Ubuntu, Isaac Sim, or PX4
version.

Confirm the configured Isaac Sim interpreter:

```bash
"$ISAACSIM_PYTHON" --version
```

Confirm that the launcher can start Isaac Sim:

```bash
isaac_run
```

Confirm that Pegasus is installed in Isaac Sim's Python environment:

```bash
"$ISAACSIM_PYTHON" -c "import pegasus.simulator; print(pegasus.simulator.__file__)"
```

## Installing This Project's Library

From the repository root, install the simulation library into Isaac Sim's
Python environment in editable mode:

```bash
"$ISAACSIM_PYTHON" -m pip install -e ./simulation
```

Editable mode makes changes under `simulation/src/drone_sim/` available without
reinstalling the package. Run the command again only when package metadata or
dependencies in `pyproject.toml` change.

Verify the installation:

```bash
"$ISAACSIM_PYTHON" -c "import drone_sim; print(drone_sim.__file__)"
```

## Running a Simulation

Run standalone scripts through the Isaac Sim interpreter wrapper from the
repository root:

```bash
isaac_run simulation/scripts/setup_stage.py
```

The stage setup script lists the USD files in `simulation/stages/` and asks
which stage to load.

## Project Layout

```text
simulation/
├── pyproject.toml          # Package metadata and build configuration
├── scripts/                # Standalone Isaac Sim entry points
├── src/
│   └── drone_sim/          # Reusable simulation library
└── stages/                 # USD stage assets
```

Use `scripts/` for executable workflows. Put reusable behavior in focused
modules under `src/drone_sim/`. Keep USD assets in `stages/` instead of embedding asset paths in
library code.
