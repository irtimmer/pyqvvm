#!/usr/bin/env python

import sys

import qemu

def main():
  app = qemu.Qemu()
  app.load(sys.argv[1])
  app.run()

if __name__ == "__main__":
  main()
