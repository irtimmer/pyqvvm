# PyQVMM

PyQVMM is a Qemu Virtual Machine Manager written in Python.
It's a wrapper around Qemu to be able to use configuration files for Qemu.
Additional plugins are provided for additional setup and cleanup of hardware, network etc.
It is not designed to manage multiple VM's on a single server, but to easier configure Qemu VM's on workstations.

## Usage

Configuration is done using YAML and follows the Qemu command line options.
Qemu will be run with the -nodefaults option and therefore some hardware like the gpu needs to be explicitly defined.

Simple configuration example:
```
qemu:
  system: x86_64
config:
  cpu: qemu64
  m: 16384
  devices:
    - driver: qxl-vga
  drives:
    - file: drive.img
      format: raw
plugins: {}
```

## Plugins

### Hugepages

The hugepage plugin will reserve hugepages before starting the VM and unreserver after the VM is exited.

Example configuration
```
config:
  m: 16384
  mem-path: /dev/hugepages
plugins:
  hugepages:
    pages: 8192 #2MB per page
```

### MacVTAP

Creates and removes a macvtap network device to directly connect the VM to your own LAN network.

Example configuration
```
config:
  devices:
    - driver: virtio-net
      netdev: network
  netdevs:
    - driver: tap
      id: network
plugins:
  macvtap:
    - name: macvtap0
      link: eth0
      id: network
```

### mdev

Create virtual devices using mdev, to be used in your VM.

Example configuration:
```
config:
  devices:
    - driver: vfio-pci
      sysfsdev: /sys/bus/pci/devices/0000:00:02.0/5c530195-909b-4123-bb33-2184453c2170
      driver: vfio-pci-nohotplug
plugins:
  mdev:
    - addr: "0000:00:02.0"
      type: i915-GVTg_V5_2
      uuid: 5c530195-909b-4123-bb33-2184453c2170 # Choose a unique GUID
```

### QMP

The QMP plugin is used to setup a connection to the QMP socket of Qemu.
This is required for the threads plugin.

Example configuration:
```
config:
  qmp:
    _value: unix:/tmp/qmp-qxl.socket
    server:
    nowait:
plugins:
  qmp:
    address: /tmp/qmp-qxl.socket
```

### Threads

Pin CPU and iothreads to specific cores.
The QMP plugin is required for this plugin to work.

Example configuration:
```
plugins:
  threads:
```
