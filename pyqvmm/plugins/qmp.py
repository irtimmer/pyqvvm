# SPDX-License-Identifier: GPL-2.0-only

import socket
import os
import time
import json

class QMP:
  def __init__(self, options):
    self.address = options['address']
    self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

  def connect(self):
    self.connected = False
    while not self.connected:
      if not os.path.exists(self.address):
        time.sleep(1)
        continue
      
      try:
        self.socket.connect(self.address)        
      except ConnectionRefusedError:
        time.sleep(1)
        continue

      self.fd = self.socket.makefile()
      self.json_read()
      self.execute({"execute": "qmp_capabilities"})

      self.connected = True

  def execute(self, cmd):
    self.json_send(cmd)
    return self.json_read()

  def json_send(self, cmd):
    self.socket.send(json.dumps(cmd).encode('utf-8'))

  def json_read(self):
    try:
      while True:
        line = json.loads(self.fd.readline())
        if not 'event' in line:
          return line
    except ValueError:
      return

  def startup(self, qemu):
    pass

  def started(self, qemu):
    self.connect()

  def destroy(self):
    pass

def getInstance(options):
  return QMP(options)
