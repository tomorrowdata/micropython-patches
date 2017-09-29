# Context

## iottlyAgent

The iottlyAgent is a small piece of software which runs on embedded devices allowing technicians to remotely jump into them, to work as if the devices were in front of them.

The iottlyAgent is written in Python 3.

For example it runs on the Raspberry Pi, on top of the default Python packages shipped by Raspbian (Raspberry Debian).

## iottlyAgent on full embedded python

The iottlyAgent also run on very constrained ARM embedded systems thanks to a full Python (3.6) embedded distribution we (TomorrowData) built from scratch to achieve a reaaally small footprint:
- 30Mb of storage space
- 6Mb or RAM when running
Our customers install this Python embedded distribution on proprietary ARM boards with less then 128Mb of flash and RAM.

## A new challenge: superstripped iottlyAgent

We are now facing a new challenge: ship the iottlyAgent on boards with 8Mb flash and 4Mb RAM, with a footprint requirement in the order of ~500Kb.

# Micropython

To achieve this main goal we are starting from the [micropython](https://github.com/micropython/micropython) distribution.
Micropython is a python port of a subset of the python standard library suited to run on highly contrained devices:
1. single board PCs (like raspberry pis) with small resource (eg 8Mb flash and 4Mb RAM) and an operating system
2. microcontroller boards (like esp8266) with 64 KiB of instruction RAM, 96 KiB of data RAM and *NO* operating system.

Our current work is about the former cathegory.


