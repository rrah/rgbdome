#include <EtherCard_STM.h>
#include <IPAddress.h>
#include <WS2812B.h>

#define LEDS 700

// LED Strip
WS2812B strip = WS2812B(LEDS);

// Network settings
static byte myip[] = { 192,168,10,6 };
static byte gwip[] = { 192,168,10,254 };
static byte mymac[] = { 0x70,0x69,0x69,0x2D,0x30,0x31 };

// Buffer for UDP data
byte Ethernet::buffer[(LEDS * 3) + 43];

void udpData(uint16_t dest_port, uint8_t src_ip[4], uint16_t src_port, const char *data, uint16_t len){
  for(uint16_t i=0; i<LEDS; i++){
    uint16_t j = i * 3;
    uint8_t r = data[j];
    uint8_t g = data[j+1];
    uint8_t b = data[j+2];
    strip.setPixelColor(i, r, g, b);
  }
  strip.show();
}

void setup(){
  // Start strip
  strip.begin();
  strip.setBrightness(255);

  if (ether.begin(sizeof Ethernet::buffer, mymac) == 0){}
  else{}
  ether.staticSetup(myip, gwip);
  ether.udpServerListenOnPort(&udpData, 1337);
}

void loop(){
  ether.packetLoop(ether.packetReceive());
}
