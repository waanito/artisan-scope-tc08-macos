#
# Copyright © 2018-2019 Pico Technology Ltd.
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
# license at: https://github.com/picotech/picosdk-python-wrappers/commit/16a4e24be5b876fc35ae55e22a354a9071dd36e6
# TC-08 STREAMING MODE EXAMPLE
# modified by waanito to run on macos

# SDK reference: https://www.picotech.com/download/manuals/usb-tc08-thermocouple-data-logger-programmers-guide.pdf



import ctypes
import numpy as np
import time
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# open unit
status["open_unit"] = tc08.usb_tc08_open_unit()
assert_pico2000_ok(status["open_unit"])
chandle = status["open_unit"]

# set mains rejection to 60 Hz (for USA)
status["set_mains"] = tc08.usb_tc08_set_mains(chandle,1)
assert_pico2000_ok(status["set_mains"])

# set up channel
# thermocouples types and int8 equivalent
# B=66 , E=69 , J=74 , K=75 , N=78 , R=82 , S=83 , T=84 , ' '=32 , X=88 
typeK = ctypes.c_int8(75)
typeT = ctypes.c_int8(84)

# alias channel numbers and buffers for readability
ch0 = 0
ch1 = 1
ch7 = 7
coldBufX = 0
ch1BufX = 1
ch7BufX = 2
#(tc08handle, ch, type)
status["set_channel"] = tc08.usb_tc08_set_channel(chandle, ch0, typeT); #setting to anything other than ' ' enables cold junction
assert_pico2000_ok(status["set_channel"])

# set channels 1 and 7
status["set_channel"] = tc08.usb_tc08_set_channel(chandle, ch1, typeK)
assert_pico2000_ok(status["set_channel"])
status["set_channel"] = tc08.usb_tc08_set_channel(chandle, ch7, typeT)
assert_pico2000_ok(status["set_channel"])

# get minimum sampling interval in ms
status["get_minimum_interval_ms"] = tc08.usb_tc08_get_minimum_interval_ms(chandle)
assert_pico2000_ok(status["get_minimum_interval_ms"])
print("min interval ms=",status["get_minimum_interval_ms"])

# set tc-08 running
status["run"] = tc08.usb_tc08_run(chandle, status["get_minimum_interval_ms"])
assert_pico2000_ok(status["run"])

# let tc08 run for a couple seconds
sleepTime = 3
print("sleeping", sleepTime)
time.sleep(sleepTime)

# collect data for 2 thermocouples plus cold junction
# [rows][columns] N.B. AFAICT one row per measurement, one col per thermocouple
temp_buffer = (ctypes.c_float * 50 * 3)()
times_ms_buffer = (ctypes.c_int32 * 50)()
overflow = ctypes.c_int16()

# usb_tc08_get_temp(
# tc08unit handle,
# ptr to readings,
# time 1st channel converted,
# buf len,
# overflow,
# channel,
# units (1=Farenheit),
# fill_missing (0 = use QNaN for missing readings)
#)
status["get_temp"] = tc08.usb_tc08_get_temp(chandle, ctypes.byref(temp_buffer[coldBufX]), ctypes.byref(times_ms_buffer), 9, ctypes.byref(overflow), 0, 1, 0)
assert_pico2000_ok(status["get_temp"])
status["get_temp"] = tc08.usb_tc08_get_temp(chandle, ctypes.byref(temp_buffer[ch1BufX]), ctypes.byref(times_ms_buffer), 9, ctypes.byref(overflow),
    ch1, 1, 0)
assert_pico2000_ok(status["get_temp"])
status["get_temp"] = tc08.usb_tc08_get_temp(chandle, ctypes.byref(temp_buffer[ch7BufX]), ctypes.byref(times_ms_buffer), 9, ctypes.byref(overflow),
    ch7, 1, 0)
assert_pico2000_ok(status["get_temp"])

# display status returns
print(status)
print("3 valuess:")
print("00",temp_buffer[coldBufX][0])
print("10",temp_buffer[ch1BufX][0])
print("20",temp_buffer[ch7BufX][0])
print("01",temp_buffer[coldBufX][1])
print("11",temp_buffer[ch1BufX][1])
print("21",temp_buffer[ch7BufX][1])
print()
'''
print("are there more?")
print("02",temp_buffer[0][2])
print("12",temp_buffer[1][2])
print("22",temp_buffer[2][2])
print("03",temp_buffer[0][3])
print("13",temp_buffer[1][3])
print("23",temp_buffer[2][3])
print("04",temp_buffer[0][4])
print("14",temp_buffer[1][4])
print("24",temp_buffer[2][4])
print("05",temp_buffer[0][5])
print("15",temp_buffer[1][5])
print("25",temp_buffer[2][5])
print("06",temp_buffer[0][6])
print("16",temp_buffer[1][6])
print("26",temp_buffer[2][6])
print("07",temp_buffer[0][7])
print("17",temp_buffer[1][7])
print("27",temp_buffer[2][7])
print("08",temp_buffer[0][8])
print("18",temp_buffer[1][8])
print("28",temp_buffer[2][8])
print("09",temp_buffer[0][9])
print("19",temp_buffer[1][9])
print("29",temp_buffer[2][9])
'''


print()
print()
print("list 0",list(temp_buffer[0]))
print("list 1",list(temp_buffer[1]))
print("list 2",list(temp_buffer[2]))
'''print("list 3",list(temp_buffer[3]))
print("list 4",list(temp_buffer[4]))
print("list 5",list(temp_buffer[5]))
print("list 6",list(temp_buffer[6]))
print("list 7",list(temp_buffer[7]))
print("list 8",list(temp_buffer[8]))
'''

sleepTime=10
print("sleep... ", sleepTime)
time.sleep(sleepTime)

status["get_temp"] = tc08.usb_tc08_get_temp(chandle, ctypes.byref(temp_buffer[ch1BufX]), ctypes.byref(times_ms_buffer), 15, ctypes.byref(overflow), ch1, 1, 1)
print("assert get temp")
assert_pico2000_ok(status["get_temp"])

# display status returns
print("status[get_temp] ch1",status["get_temp"])

status["get_temp"] = tc08.usb_tc08_get_temp(chandle, ctypes.byref(temp_buffer[ch7BufX]), ctypes.byref(times_ms_buffer), 15, ctypes.byref(overflow), ch7, 1, 1)
assert_pico2000_ok(status["get_temp"])

# display status returns
print("status[get_temp] ch7",status["get_temp"])
print("list 1",list(temp_buffer[ch1BufX]))
print("list 2",list(temp_buffer[ch7BufX]))
print("list 0",list(temp_buffer[coldBufX]))

sleepTime=1
print("sleep... ", sleepTime)
time.sleep(sleepTime)


# stop unit
status["stop"] = tc08.usb_tc08_stop(chandle)
assert_pico2000_ok(status["stop"])

# close unit
status["close_unit"] = tc08.usb_tc08_close_unit(chandle)
assert_pico2000_ok(status["close_unit"])

# display status returns
print(status)
