# SPDX-License-Identifier: LGPL-2.1-or-later

import os

class Vfio:
  def __init__(self, options):
    self.devices = options

  def startup(self, qemu):
    for device in self.devices:
      data = open('/sys/bus/pci/devices/0000:%s/uevent'%(device['host'])).read()
      conf = dict((line.split("=", 1) for line in data.splitlines()))

      if 'DRIVER' not in conf or conf['DRIVER'] != 'vfio-pci':
        path = '/sys/bus/pci/devices/0000:%s/driver/unbind'%(device['host'])
        if os.path.exists(path):
          with open(path, 'w') as f:
            f.write('0000:%s\n'%(device['host']))

        with open('/sys/bus/pci/drivers/vfio-pci/new_id', 'w') as f:
          f.write(conf['PCI_ID'].replace(':', ' '))

  def destroy(self):
    for device in self.devices:
      if device['rebind']:
        with open('/sys/bus/pci/drivers/vfio-pci/unbind', 'w') as f:
          f.write('0000:%s\n'%(device['host']))

        with open('/sys/bus/pci/drivers_probe', 'w') as f:
          f.write('0000:%s\n'%(device['host']))

def getInstance(options):
  return Vfio(options)
