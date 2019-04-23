# SPDX-License-Identifier: GPL-2.0-only

import os

class Vfio:
  def __init__(self, options):
    self.devices = options

  def startup(self, qemu):
    for device in self.devices:
      for host in os.listdir('/sys/bus/pci/devices/0000:%s/iommu_group/devices'%(device['host'])):
        data = open('/sys/bus/pci/devices/%s/uevent'%(host)).read()
        conf = dict((line.split("=", 1) for line in data.splitlines()))

        if 'DRIVER' not in conf or conf['DRIVER'] != 'vfio-pci':
          path = '/sys/bus/pci/devices/%s/driver/unbind'%(host)
          if os.path.exists(path):
            with open(path, 'w') as f:
              f.write('%s\n'%(host))

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
