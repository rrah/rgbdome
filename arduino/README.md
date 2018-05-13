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