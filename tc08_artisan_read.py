#!/usr/bin/env python3
#print("123.4,234.5") # test line

# Copyright © 2018-2019   Pico Technology Ltd.
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
# license at: https://github.com/picotech/picosdk-python-wrappers/commit/16a4e24be5b876fc35ae55e22a354a9071dd36e6

# PicoTech TC-08 Python SINGLE MODE EXAMPLE
# original at https://github.com/picotech/picosdk-python-wrappers/blob/master/usbtc08Examples/tc08SingleModeExample.py
##################################################################################
# modified by waanito to run on macos 10.15 (probably will run on 10.16 but not tested) and supply temperatures in artisan-scope external prog format
##################################################################################

## N.B.## Variables LD_LIBRARY_PATH / DYLD_LIBRARY_PATH are not passed to the environment of a child process on macOS if System Integrity Protect (SIP) is enabled so need import here.
#https://stackoverflow.com/questions/60126159/how-to-set-ld-library-path-dyld-library-path-on-macos
import os
os.environ["DYLD_LIBRARY_PATH"] = "/Library/Frameworks/PicoSDK.framework/Libraries/libusbtc08/"

# test paths
#print("PATH: ",os.environ.get("PATH"))
#print("LD_LIBRARY_PATH: ", os.environ.get("LD_LIBRARY_PATH"))
#print("DYLD_LIBRARY_PATH: ",os.environ.get("DYLD_LIBRARY_PATH"))

import ctypes
from picosdk.usbtc08 import usbtc08 as tc08

# open unit
chandle = tc08.usb_tc08_open_unit()

# set mains rejection to 60 Hz (USA)
tc08.usb_tc08_set_mains(chandle,1)

# set up channel
# thermocouple types and int8 equivalent
# B=66 , E=69 , J=74 , K=75 , N=78 , R=82 , S=83 , T=84 , ' '=32 , X=88
typeK = ctypes.c_int8(75)
typeT = ctypes.c_int8(84)

#status["set_channel"] = tc08.usb_tc08_set_channel(chandle, 0, typeK)# not used for artisan

# environment temp, beean temp channels
ETch = 4
BTch = 5
tc08.usb_tc08_set_channel(chandle, ETch, typeK)
tc08.usb_tc08_set_channel(chandle, BTch, typeK)

# get one temperature reading of each channel
# buffers:
temp = (ctypes.c_float * 9)()
overflow = ctypes.c_int16(0)
# see usbtc08.h in framework for typedefs
units = tc08.USBTC08_UNITS["USBTC08_UNITS_FAHRENHEIT"]
# get the readings into temp
tc08.usb_tc08_get_single(chandle,ctypes.byref(temp), ctypes.byref(overflow), units)
# print for artisan
print(round(temp[ETch],1), ",", round(temp[BTch],1), sep="")

# close unit
tc08.usb_tc08_close_unit(chandle)
