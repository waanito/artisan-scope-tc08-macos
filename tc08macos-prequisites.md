## PicoTech TC08 running on macos, prequisites:
* need PicoTech SDK installed from here: 
 https://www.picotech.com/downloads/_lightbox/pico-software-development-kit-64bit

* then also SDK installed from bash like so
pip install picosdk

* from bash set path var
 DYLD_FALLBACK_LIBRARY_PATH 
 not DYLD_LIBRARY_PATH per this
 https://stackoverflow.com/questions/3146274/is-it-ok-to-use-dyld-library-path-on-mac-os-x-and-whats-the-dynamic-library-s/3172515#3172515
 like so:
export DYLD_FALLBACK_LIBRARY_PATH=$DYLD_FALLBACK_LIBRARY_PATH:/Library/Frameworks/PicoSDK.framework/Libraries/libusbtc08

or add that export to ~/.bash_profile

## References
* PicoTech Github https://github.com/picotech
* programmers manual https://www.picotech.com/download/manuals/usb-tc08-thermocouple-data-logger-programmers-guide.pdf

