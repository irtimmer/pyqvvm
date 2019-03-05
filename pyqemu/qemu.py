# SPDX-License-Identifier: LGPL-2.1-or-later

import yaml
import subprocess
import importlib

ROOT_OPTION = {
  'device': 'driver',
  'netdev': 'driver'
}

class Qemu:
  def load(self, file):
    cfg = yaml.load(open(file))
    self.config = cfg['config']
    self.qemu = cfg['qemu']
    self.plugins = []
    for key in cfg['plugins']:
      plugin = importlib.import_module('plugins.' + key).getInstance(cfg['plugins'][key])
      self.plugins.append(plugin)

  def _option(self, key, value):
    return key if value == None else '%s=%s' % (key, value)

  def _enc_option(self, key, options):
    if isinstance(options, dict):
      root_option = ROOT_OPTION[key] if key in ROOT_OPTION else 'value'
      args = [self._option(k, v) for (k, v) in options.items() if k != root_option]
      if root_option in options:
        args.insert(0, options[root_option])

      return ['-' + key, ','.join(args) ]
    else:
      return ['-' + key, str(options)]

  def get_arguments(self):
    args = ['-nodefaults']
    for k in self.config:
      if isinstance(self.config[k], list):
        for i in self.config[k]:
          args.extend(self._enc_option(k[:-1], i))
      else:
        args.extend(self._enc_option(k, self.config[k]))

    return args

  def run(self):
    cmd = ['/usr/bin/qemu-system-%s'%(self.qemu['system'])]
    cmd.extend(self.get_arguments())
    print(' '.join(cmd))

    try:
      for plugin in self.plugins:
        plugin.startup()

      process = subprocess.Popen(cmd)
      process.wait()
    finally:
      for plugin in self.plugins:
        plugin.destroy()
