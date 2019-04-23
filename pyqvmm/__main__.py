#!/usr/bin/env python

# SPDX-License-Identifier: GPL-2.0-only

import sys

import qemu

def main():
  app = qemu.Qemu()
  app.load(sys.argv[1])
  app.run()

if __name__ == "__main__":
  main()
