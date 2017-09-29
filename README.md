# Context

## iottlyAgent

The iottlyAgent is a small piece of software (by TomorrowData) which runs on embedded devices allowing technicians to remotely jump into them, to remotely work with such devices as if they were in front of them.

The iottlyAgent is written in Python 3, beacuse with python we can give great flexibility to the technicians which can easily write their own custom functions for the management and monitoring of the embedded devices.

This of course means that we need Python running on the embedded devices. For example, when on a Raspberry Pi, the iotlyAgent runs on top of the default Python packages shipped by Raspbian (Raspberry Debian).

## iottlyAgent on full python embedded

The iottlyAgent also run on very constrained ARM embedded systems thanks to a full Python (3.6) embedded distribution we (TomorrowData) built from scratch to achieve a reaaally small footprint:
- 30Mb of storage space
- 6Mb or RAM when running

Our customers install this Python embedded distribution on proprietary ARM boards with less then 128Mb of flash and RAM.

# A new challenge: superstripped iottlyAgent

We are now facing a new challenge: ship the iottlyAgent on boards with 8Mb flash and 4Mb RAM, with a footprint requirement in the order of ~500Kb.

## Micropython

To achieve this main goal we are starting from the [micropython](https://github.com/micropython/micropython) distribution.
Micropython is a port of a **subset of the python standard library** suited to run on highly constrained devices:
1. single board PCs (like raspberry pis) with small resources (eg 8Mb flash and 4Mb RAM) and the Linux operating system
2. microcontroller boards (like esp8266, with 64 KiB of instruction RAM, 96 KiB of data RAM) and **NO** operating system.

Our current work is about the former cathegory.

We use a single executable standalone build of micropython (`230 Kb`).

## Porting the iottlyAgent on micropython

Given that only a subset of the python standard library is available on micropython we need to make a porting of the iottlyAgent code to make it running on micropython.

## Multithreading

iottlyAgent heavily relies on multithreading to perform a lot of tasks in parallel:
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

Long story short, to make the porting of the iottlyAgent as smooth as possible, we need to ...

# Implement `threading` and `queue` APIs in micropython

Which is actually your task ... :)

More precisely, provide a pure (micro)python implementation of:
- `threading`: https://docs.python.org/3.5/library/threading.html
- `queue`: https://docs.python.org/3.5/library/queue.html

The implementation is to be based on top of the two aforementioned low level micropython apis (at least for what concerns `_thread`, while `heapqueue` is up to you).

The code should be well documented (comments) and production grade.

## Validation

To validate the implementation we'll use the above [`test_threading.py`](https://github.com/tomorrowdata/micropython-patches/blob/master/test_threading.py) file.

The script is tested in python 3.5 where it produces the following output:
```
$ python3 test_threading.py 
<_MainThread(MainThread, started 140104763766528)> 2017-09-29T14:01:20 Started.
<Thread(t1, started 140104739841792)> 2017-09-29T14:01:20 enqueue 0
<Thread(t2, started 140104731449088)> 2017-09-29T14:01:20 dequeue 0
<Thread(t1, started 140104739841792)> 2017-09-29T14:01:21 enqueue 1
<Thread(t2, started 140104731449088)> 2017-09-29T14:01:21 dequeue 1
<Thread(t1, started 140104739841792)> 2017-09-29T14:01:22 enqueue 2
<Thread(t2, started 140104731449088)> 2017-09-29T14:01:22 dequeue 2
<Thread(t1, started 140104739841792)> 2017-09-29T14:01:23 enqueue 3
<Thread(t2, started 140104731449088)> 2017-09-29T14:01:23 dequeue 3
<Thread(t1, started 140104739841792)> 2017-09-29T14:01:24 finished iterations, exiting.
<Thread(t2, started 140104731449088)> 2017-09-29T14:01:24 received stop message, exiting.
<_MainThread(MainThread, started 140104763766528)> 2017-09-29T14:01:24 finished.
```
The specific goal of the requested implementation is to produce the exact same output with micropython on an ARM machine:
```
$ micropython test_threading.py 
```
Minor changes to the test file (like `import time as time -> import utime as time`) will be OK.

If you really really need to change something to the test file, please motivate it.


## Development environment

### Code management

- Fork this repo on your github account
- commit and push your work to your repo
- finally make a pull request to this repo to submit your work.

### Running environment

To let you test your code in an ARM environment, we provide you with a micropython installed in a cloud ARM server. 
You can access it via ssh: 
- IP: `163.172.186.107`
- user: `builder`
- key: provide us with your public ssh key and we will set it into the server, so to allow access to you.

Once on the server you can simply run:
- `python3`
- `micropython`

## That's all

Do not esitate to contact us for any doubt, or to discuss your approach.

Enjoy this challenge!
