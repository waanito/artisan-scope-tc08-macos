## Using PicoTech TC08 with Artisan-Scope running on macos:
* install PicoTech SDK framework from here:  
 [https://www.picotech.com/downloads/_lightbox/pico-software-development-kit-64bit](https://www.picotech.com/downloads/_lightbox/pico-software-development-kit-64bit)

* python can't find the framework path until this is done from CLI:

``` pip3 install picosdk ```

* edit tc08_artisan_read.py to suit your environment

* make the script executable
  
```chmod u+x ./tc08_artisan_read.py```
 
* confirm that you can run the script from CLI

```./tc08_artisan_read.py```

* in artisan-scope cmd-D to bring up Device Assignment, select Prog,   
and point at tc08_artisan_read.py in External Program

* click ON in artisan to confirm the ET and BT are displaying


## References
* [PicoTech Github](https://github.com/picotech)
* [USB-TC08 programmers manual](https://www.picotech.com/download/manuals/usb-tc08-thermocouple-data-logger-programmers-guide.pdf)

