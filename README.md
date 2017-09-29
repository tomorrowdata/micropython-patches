# Context

## iottlyAgent

The iottlyAgent is a small piece of software (by TomorrowData) which runs on embedded devices allowing technicians to remotely jump into them, to remotely work with such devices as if they were in front of them.

The iottlyAgent is written in Python 3, beacuse with python we can give great flexibility to the technicians which can easily write their own custom functions for the management and monitoring of the embedded devices.

This means we need Python running on the embedded devices. For example it runs on the Raspberry Pi, on top of the default Python packages shipped by Raspbian (Raspberry Debian).

## iottlyAgent on full embedded python

The iottlyAgent also run on very constrained ARM embedded systems thanks to a full Python (3.6) embedded distribution we (TomorrowData) built from scratch to achieve a reaaally small footprint:
- 30Mb of storage space
- 6Mb or RAM when running

Our customers install this Python embedded distribution on proprietary ARM boards with less then 128Mb of flash and RAM.

# A new challenge: superstripped iottlyAgent

We are now facing a new challenge: ship the iottlyAgent on boards with 8Mb flash and 4Mb RAM, with a footprint requirement in the order of ~500Kb.

## Micropython

To achieve this main goal we are starting from the [micropython](https://github.com/micropython/micropython) distribution.
Micropython is a python port of a **subset of the python standard library** suited to run on highly constrained devices:
1. single board PCs (like raspberry pis) with small resource (eg 8Mb flash and 4Mb RAM) and the Linux operating system
2. microcontroller boards (like esp8266) with 64 KiB of instruction RAM, 96 KiB of data RAM and **NO** operating system.

Our current work is about the former cathegory.

## porting iottlyAgent on micropython

Given that only a subset of the python standard library is available on micropython we need to make a porting of the iottlyAgent code to make it running on micropython.

## Multithreading

iottlyAgent heavily relies on multithreading to perform in parallel a lot of tasks:
- MQTT communication with iottlyCloud
- async execution of scheduled tasks
- async execution of long running tasks triggered by external commands
- over-the-air self upgrade

Specifically the iottlyAgent code makes use of the following packages and the related APIs:
- `threading`
- `queue`

Hence, multithreading support in micropython is crucial for the success of the port.

## Multithreading in micropython

It turns out that micropython implements two low level apis which are fundamental to multithreading:
- `_thread`: an example [here](https://forum.micropython.org/viewtopic.php?t=1864)
- `heapqueue`: [here](http://docs.micropython.org/en/latest/wipy/library/uheapq.html)

Unfortunaltely it does not implement the full high level APIs of `threading` and `queue`.

Long story short, to make the porting of the iottlyAgent as smooth as possible, we need ...

# Implement `threading` and `queue` APIs in micropython




