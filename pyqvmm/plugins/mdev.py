# SPDX-License-Identifier: GPL-2.0-only

class Mdev:
  def __init__(self, options):
    self.devices = options

  def startup(self, qemu):
    for device in self.devices:
      with open('/sys/bus/pci/devices/%s/mdev_supported_types/%s/create'%(device['addr'], device['type']), 'w') as f:
        f.write(device['uuid'])

  def started(self, qemu):
    pass

  def destroy(self):
    for device in self.devices:
      with open('/sys/bus/pci/devices/%s/%s/remove'%(device['addr'], device['uuid']), 'w') as f:
        f.write('1')

def getInstance(options):
  return Mdev(options)
