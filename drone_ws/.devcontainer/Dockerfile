ARG ROS_DISTRO=jazzy

# ---------------------------------------------------------------------------
# Stage 1: build the Micro XRCE-DDS Agent.
#
# The upstream snap package cannot be installed in a container, so it has to be
# compiled. The CMake superbuild pulls and compiles Fast DDS, which makes this
# by far the slowest step — and it leaves a ~500 MB build tree behind. Keeping
# it in its own stage means only the installed artifacts reach the final image,
# and editing the apt list below never triggers a recompile.
# ---------------------------------------------------------------------------
FROM osrf/ros:${ROS_DISTRO}-desktop AS xrce-builder

# Micro XRCE-DDS Agent release, the bridge to the PX4 uxrce_dds_client.
ARG XRCE_AGENT_VERSION=v2.4.3

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
    && rm -rf /var/lib/apt/lists/*

# `--install` is a separate step because the default target only compiles, and
# in superbuild mode the install rule does not exist until after that build.
# DESTDIR stages the result so the next stage copies only these files, not the
# base image's own /usr/local.
RUN git clone --depth 1 --branch ${XRCE_AGENT_VERSION} \
        https://github.com/eProsima/Micro-XRCE-DDS-Agent.git /tmp/xrce-agent \
    && cmake -S /tmp/xrce-agent -B /tmp/xrce-agent/build \
        -DCMAKE_BUILD_TYPE=Release \
        -DUAGENT_BUILD_EXECUTABLE=ON \
    && cmake --build /tmp/xrce-agent/build --parallel "$(nproc)" \
    && DESTDIR=/staging cmake --install /tmp/xrce-agent/build \
    # Fail the stage loudly if the agent did not actually get installed.
    && test -x /staging/usr/local/bin/MicroXRCEAgent

# ---------------------------------------------------------------------------
# Stage 2: the development image.
# ---------------------------------------------------------------------------
FROM osrf/ros:${ROS_DISTRO}-desktop

ARG ROS_DISTRO
ARG USERNAME=dnav
ARG USER_UID=1000
ARG USER_GID=1000

ENV DEBIAN_FRONTEND=noninteractive

# Build toolchain, ROS tooling, and the handful of CLI tools worth having when
# debugging DDS traffic from inside the container.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        clang-format \
        cmake \
        gdb \
        git \
        iproute2 \
        iputils-ping \
        less \
        nano \
        micro \
        python3-colcon-common-extensions \
        python3-colcon-clean \
        python3-pip \
        python3-rosdep \
        python3-vcstool \
        ros-dev-tools \
        sudo \
    && rm -rf /var/lib/apt/lists/*

COPY --from=xrce-builder /staging/usr/local /usr/local
RUN ldconfig /usr/local/lib/ \
    # Fail the layer loudly if the agent did not actually land on PATH.
    && command -v MicroXRCEAgent

# Create a user whose UID/GID match the host, so files written into the bind
# mount are not owned by root. Ubuntu 24.04 ships an `ubuntu` user at UID 1000,
# which has to go first when the host UID collides with it.
RUN if getent passwd ${USER_UID} >/dev/null; then \
        userdel -r "$(getent passwd ${USER_UID} | cut -d: -f1)" 2>/dev/null || true; \
    fi \
    && groupadd -f -g ${USER_GID} ${USERNAME} \
    && useradd -m -u ${USER_UID} -g ${USER_GID} -s /bin/bash ${USERNAME} \
    # dialout for serial links to real flight controllers later, video for GPU
    # access from RViz. Skip any group this base image does not define.
    && for grp in dialout video plugdev; do \
        getent group "$grp" >/dev/null && usermod -aG "$grp" ${USERNAME}; \
    done \
    && echo "${USERNAME} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

USER ${USERNAME}
WORKDIR /drone_ws

# Source the ROS 2 installation and, when it exists, the workspace overlay.
RUN printf '%s\n' \
        "source /opt/ros/${ROS_DISTRO}/setup.bash" \
        "[ -f /drone_ws/install/setup.bash ] && source /drone_ws/install/setup.bash" \
        >> /home/${USERNAME}/.bashrc

CMD ["/bin/bash"]
