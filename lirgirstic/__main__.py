#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

sys.path.append(".")

from lirgirstic.lirc import lircd_start
from time import sleep

def main():
    lircd_start()
    while True:
        sleep(0.1)

if __name__ == '__main__':
    main()
