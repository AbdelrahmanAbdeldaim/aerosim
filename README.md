# Drone Navstack
Drone Navstack is a Sim-to-Real autonomous drone project powered by ROS 2 and NVIDIA Isaac Sim. Documenting the journey from high-level simulation control to physical flight.

## Isaac Sim Docker Setup

Full reference: <https://docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/install_container.html>

### Prerequisites

1. **Install Docker**

   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh

   # Post-install
   sudo groupadd docker
   sudo usermod -aG docker $USER
   newgrp docker
   ```

2. **Install NVIDIA Container Toolkit**

   ```bash
   curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
     && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
     sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
     sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

   sudo apt-get update
   sudo apt-get install -y nvidia-container-toolkit
   sudo nvidia-ctk runtime configure --runtime=docker
   sudo systemctl restart docker
   ```

3. **Verify**

   ```bash
   docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi
   ```

### Pull the Isaac Sim Image

```bash
docker pull nvcr.io/nvidia/isaac-sim:5.1.0
```

### Create Host Cache Directories

```bash
mkdir -p ~/docker/isaac-sim/cache/main/ov
mkdir -p ~/docker/isaac-sim/cache/main/warp
mkdir -p ~/docker/isaac-sim/cache/computecache
mkdir -p ~/docker/isaac-sim/config
mkdir -p ~/docker/isaac-sim/data/documents
mkdir -p ~/docker/isaac-sim/data/Kit
mkdir -p ~/docker/isaac-sim/logs
mkdir -p ~/docker/isaac-sim/pkg
sudo chown -R 1234:1234 ~/docker/isaac-sim
```

### Run with Docker Compose

```bash
cd docker
docker compose up
```

The container automatically starts Isaac Sim in headless mode with livestreaming enabled.

### Connect via WebRTC Streaming Client

1. Download the [Isaac Sim WebRTC Streaming Client](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/download.html#isaac-sim-latest-release) for your platform from the Latest Release section.
2. Run the Isaac Sim WebRTC Streaming Client app.

   On Linux, you may need to extract and fix sandbox permissions:

   ```bash
   ./isaacsim-webrtc-streaming-client-1.1.5-linux-x64.AppImage --appimage-extract
   sudo chmod 4755 squashfs-root/chrome-sandbox
   ./squashfs-root/AppRun
   ```
3. Enter the IP address of the machine running the Isaac Sim container and click **Connect**.
