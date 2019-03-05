#!/usr/bin/env python

# SPDX-License-Identifier: LGPL-2.1-or-later

import sys

import qemu

def main():
  app = qemu.Qemu()
  app.load(sys.argv[1])
  app.run()

if __name__ == "__main__":
  main()
