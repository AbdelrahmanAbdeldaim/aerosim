# Drone Navstack Simulation

Isaac Sim scripts, USD stages, and reusable Python utilities for the Drone
Navstack project.

The Python distribution and import names are intentionally different:

| Purpose | Name |
| --- | --- |
| Package installed by `pip` | `drone-navstack-sim` |
| Package imported by Python | `drone_sim` |

## Prerequisites

Complete the following steps in order. Each one links to the upstream guide;
the notes summarize what to do and call out project-specific settings.

1. [Install NVIDIA Isaac Sim 5.1](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/install_workstation.html) using NVIDIA's official workstation installation guide. Download and extract the Linux archive, run `./post_install.sh`, and verify the installation using `./isaac-sim.selector.sh`.
2. [Configure the environment variables](https://pegasussimulator.github.io/PegasusSimulator/source/setup/installation.html#configuring-the-environment-variables). Add `ISAACSIM_PATH`, `ISAACSIM_PYTHON`, `ISAACSIM`, and the `isaac_run` function to your shell configuration, then open a new terminal.
3. [Install Pegasus Simulator](https://pegasussimulator.github.io/PegasusSimulator/source/setup/installation.html#installing-the-pegasus-simulator). Clone Pegasus, register its `extensions/` directory in Isaac Sim, enable the extension, and install `pegasus.simulator` with Isaac Sim's Python interpreter.
4. Install PX4 Autopilot v1.17 for software-in-the-loop flight control (see below).
5. Register the PX4 repository path with Pegasus (see below).

### Install PX4 Autopilot v1.17

Install the PX4 build dependencies and clone the v1.17 release. These commands
clone into your home directory; if you use a different location, remember it for
the Pegasus configuration step.

```bash
sudo apt install git make cmake python3-pip
cd ~
git clone https://github.com/PX4/PX4-Autopilot.git
cd PX4-Autopilot
git checkout v1.17.0
git submodule update --init --recursive
bash ./Tools/setup/ubuntu.sh
```

After installation is done, build PX4 SITL for use with Pegasus:

```bash
cd ~/PX4-Autopilot
make px4_sitl_default none
```

### Register the PX4 path with Pegasus

Pegasus launches a PX4 software-in-the-loop instance to fly the drone, so it
needs to know where the PX4 repository lives. The path defaults to
`~/PX4-Autopilot`; update it only if you cloned PX4 somewhere else.

Edit the `px4_dir` key in the Pegasus extension configuration file, located at
`extensions/pegasus.simulator/config/configs.yaml` inside your Pegasus clone.

## Verifying the Setup

Confirm the configured Isaac Sim interpreter:

```bash
"$ISAACSIM_PYTHON" --version
```

Confirm that the launcher can start Isaac Sim:

```bash
isaac_run
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

Run standalone examples through the Isaac Sim interpreter wrapper from the
examples folder. Available examples are:

<table border="1" cellpadding="6" cellspacing="0">
  <thead>
    <tr>
      <th>Example</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>empty_scene_with_walls.py</code></td>
      <td>Starts Isaac Sim in GUI mode and loads<br>an empty walled environment (Pegasus "Box Room")<br>containing a single PX4 quadrotor.
    </tr>
  </tbody>
</table>

Run an example from the repository root:

```bash
isaac_run simulation/examples/empty_scene_with_walls.py
```

Replace `empty_scene_with_walls.py` with the filename of the example you want
to run.
