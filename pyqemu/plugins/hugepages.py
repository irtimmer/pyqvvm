# SPDX-License-Identifier: LGPL-2.1-or-later

import os

class Hugepages:
  def __init__(self, options):
    self.options = options

  def startup(self, qemu):
    size = 0
    with open('/proc/sys/vm/nr_hugepages', 'r') as f:
      size = int(f.read())

    with open('/proc/sys/vm/nr_hugepages', 'w') as f:
      f.write(str(size + self.options.pages))

  def destroy(self):
    size = 0
    with open('/proc/sys/vm/nr_hugepages', 'r') as f:
      size = int(f.read())

    if size > self.options.pages:
      with open('/proc/sys/vm/nr_hugepages', 'w') as f:
        f.write(str(size - self.options.pages))

def getInstance(options):
  return Hugepages(options)
