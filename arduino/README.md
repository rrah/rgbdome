# RGB Dome Arduino code

## nanostrand
Controller for Arduino Nano using enc28j60 ethernet chip

### Requirements
- Ethercard
- Neopixel

### Limits
- ~240 LED's before running out of memory

## stmstrand
Controller for STM32 using enc28j60 ethernet chip and Arduino_STM32

### Requirements
- Arduino_STM32
- Ethercard_STM
- WS2812B, modified to use SPI 2

### Limits
- ~700 LED's before failing to run at all
- 484 LED's per UDP packet

### Connections
PA5 - SCK
PA6 - SO
PA7 - SI
PA8 - CS
PB15 - LEDs

### Notes
The 3v3 reg on "Blue Pill" STM32 boards is somewhat cheap, and some instability has been experienced when using the onboard 3v3 to power the ENC28J60. Using an external 3v3 reg (e.g, LD1117V33) between the onboard 5v and the ENC28J60's 3v3 seems to fix these instabilities.

For futher information, see:
http://wiki.stm32duino.com/index.php?title=Blue_Pill#Known_issues
https://electronics.stackexchange.com/questions/52349/why-is-ethernet-so-power-hungry

### Flashing controller
- Download and nstall Arduino IDE
- Download and install ST-LINK drivers (https://www.st.com/en/development-tools/stsw-link009.html)
- Download lastest Arduino_STM32 by Roger Clark from Github (https://github.com/rogerclarkmelbourne/Arduino_STM32) and place into Arduino Hardware folder (default %programfiles(x86)%\Arduino\Hardware)
- Run the IDE, and on the Tools menu, select the Boards manager, and install the Arduino SAM boards (Cortex-M3) from the list of available boards. You must do this step, it installs the arm-none-eabi-g++ toolchain!
- Run stm32-setup.py, following the instructions in the console