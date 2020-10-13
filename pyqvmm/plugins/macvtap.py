# SPDX-License-Identifier: GPL-2.0-only

import os
import subprocess

class Macvtap:
  def __init__(self, options):
    self.networks = options

  def startup(self, qemu):
    for network in self.networks:
      print(network)
      subprocess.call(['ip', 'link', 'add', 'link', network['link'], 'name', network['name'], 'type', 'macvtap'])
      subprocess.call(['ip', 'link', 'set', network['name'], 'address', network['mac'], 'up'])
      index = open('/sys/class/net/%s/ifindex'%(network['name'])).read()
      fd = os.open('/dev/tap%d'%(int(index)), os.O_RDWR)
      for netdev in qemu.config['netdevs']:
        if netdev['id'] == network['id']:
          netdev['fd'] = fd

      qemu.register_fd(fd);

  def started(self, qemu):
    pass

  def destroy(self):
    for network in self.networks:
      subprocess.call(['ip', 'link', 'del', 'dev', network['name']])

def getInstance(options):
  return Macvtap(options)
