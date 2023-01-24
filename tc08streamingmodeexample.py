# Copyright © 2018-2019 Pico Technology Ltd.
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
# license at: https://github.com/picotech/picosdk-python-wrappers/commit/16a4e24be5b876fc35ae55e22a354a9071dd36e6

# PicoTech TC-08 Python STREAMING MODE EXAMPLE
# original at https://github.com/picotech/picosdk-python-wrappers/blob/master/usbtc08Examples/tc08StreamingModeExample.py
# modified by waanito to run on macos 10.15 (probably will run on 10.16 but not tested)
# also modified to work more like the C/C++ version https://github.com/picotech/picosdk-c-examples/blob/master/usbtc08/usbtc08Con/usbtc08Con.c which shows continuously but w/o the single reading which will do in a separate file and also without keyboard interrupt

# SDK reference: https://www.picotech.com/download/manuals/usb-tc08-thermocouple-data-logger-programmers-guide.pdf



import ctypes
#import numpy as np  # not used
import time
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok

USBTC08_MAX_CHANNELS = 8

# numberOfReadings = 0 # Number of readings to collect in streaming mode # not used
readingsCollected = 0 # Number of readings collected at a time in streaming mode
totalReadings = [0] * (USBTC08_MAX_CHANNELS + 1) # Total readings collected in streaming mode (allows for all 8 channels + CJN)
readingsDisplayed = 0

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

print("===============================")

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

# alias channel numbers for readability
# it's memory wasteful, when using only a couple chennels, but using a buffer with all 9 channels avoids buffer indices being different from channel indices
cjn = 0
ch1 = 1
ch7 = 7


# usb_tc08_set_channel(tc08handle, ch, type)
# enable cold junction
status["set_channel"] = tc08.usb_tc08_set_channel(chandle, cjn, typeT); #setting to anything other than ' ' enables cold junction
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


# get number of readings to do from user
maxReadings = 50
readingsToDo = 0
while True:
  print("Enter number of readings to do (1-",maxReadings,"):", end=' ')
  readingsToDo = int (input())
  if readingsToDo > 0 and readingsToDo <= maxReadings:
    break

# set tc-08 running
status["run"] = tc08.usb_tc08_run(chandle, status["get_minimum_interval_ms"])
assert_pico2000_ok(status["run"])



# collect data for 2 thermocouples plus cold junction
# [rows][columns] N.B. the guide doesn't say but AFAICT one row per measurement, one col per thermocouple
# N.B.: rows,cols
temp_buffer = (ctypes.c_float * readingsToDo * (USBTC08_MAX_CHANNELS +1))() # one extra for cold junction
times_ms_buffer = (ctypes.c_int32 * readingsToDo)()
overflow = ctypes.c_int16()

# diag
#print("buffer columns",len(temp_buffer))
#print("CJN rows",len(temp_buffer[cjn]))
#print("ch1 rows",len(temp_buffer[ch1]))
#print("ch7 rows",len(temp_buffer[ch7]))
#print("ms len",len(times_ms_buffer))

# print output header
print("                              cycle");
print("                              read   reading");
print(" T(ms)  CJN     Ch1     Ch7   index  number");

# collect data
collectionTime = (status["get_minimum_interval_ms"]/1000 * 3) + 0.1
collectionTime=1
for i in range( readingsToDo ):
  time.sleep(collectionTime) # give tc08 time to collect some data

  # usb_tc08_get_temp(
  #   tc08unit handle,
  #   ptr to readings,
  #   time 1st channel converted,
  #   buf len,
  #   overflow,
  #   channel,
  #   units (1=Farenheit),
  #   fill_missing (0 = use QNaN for missing readings)
  #)
  
  # get cold junction
  readingsCollected = 0
  cyclesToRead = 0
  while True:
    cyclesToRead += 1
    readingsCollected = tc08.usb_tc08_get_temp(chandle, ctypes.byref(temp_buffer[cjn]), ctypes.byref(times_ms_buffer), 9, ctypes.byref(overflow), cjn, 1, 0)
    if readingsCollected != 0:
      break
  if readingsCollected < 0: # < 0 is an error returned
    print("error reading cjn")
    #shut down tco8
    tc08.usb_tc08_stop(chandle)
    tc08.usb_tc08_close_unit(chandle)
    quit()
  totalReadings[cjn] = totalReadings[cjn] +  readingsCollected
  
  # get channel 1
  readingsCollected = 0
  cyclesToRead = 0
  while True:
    cyclesToRead += 1
    readingsCollected = tc08.usb_tc08_get_temp(chandle, ctypes.byref(temp_buffer[ch1]), ctypes.byref(times_ms_buffer), 9, ctypes.byref(overflow), ch1, 1, 0)
    if readingsCollected != 0:
      break
  if readingsCollected < 0: # < 0 is an error returned
    print("error reading ch1")
    #shut down tco8
    tc08.usb_tc08_stop(chandle)
    tc08.usb_tc08_close_unit(chandle)
    quit()
  totalReadings[ch1] = totalReadings[ch1] +  readingsCollected
  
  # get channel 7
  readingsCollected = 0
  cyclesToRead = 0
  while True:
    cyclesToRead += 1
    readingsCollected =  tc08.usb_tc08_get_temp(chandle, ctypes.byref(temp_buffer[ch7]), ctypes.byref(times_ms_buffer), 9, ctypes.byref(overflow),
        ch7, 1, 0)
    if readingsCollected != 0:
      break
  if readingsCollected < 0: # < 0 is an error returned
    print("error reading ch7")
    #shut down tco8
    tc08.usb_tc08_stop(chandle)
    tc08.usb_tc08_close_unit(chandle)
    quit()
  totalReadings[ch7] = totalReadings[ch7] +  readingsCollected
  
  # print this cycle's readings
  readingsToPrint = min( readingsCollected,
                         readingsToDo,
                         (readingsToDo  - readingsDisplayed)
                       )
                       # avoid bad index when readingsCollected > readingsToDo and/or displaying more readings than asked for
  
  for j in range(readingsToPrint):
    print("%5d" % (times_ms_buffer[j]), end = ' ')
    print("%5.4f" % (temp_buffer[cjn][j]), end = ' ')
    print("%5.4f" % (temp_buffer[ch1][j]), end = ' ')
    print("%5.4f" % ( temp_buffer[ch7][j]), end = ' ')
    print("%3d" % (j), end = ' ')
    readingsDisplayed += 1
    print("%7d" % (readingsDisplayed))
    
  if totalReadings[cjn] >= readingsToDo:
    break

# stop unit
status["stop"] = tc08.usb_tc08_stop(chandle)
assert_pico2000_ok(status["stop"])

# close unit
status["close_unit"] = tc08.usb_tc08_close_unit(chandle)
assert_pico2000_ok(status["close_unit"])

