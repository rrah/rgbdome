#include <EtherCard_STM.h>
#include <IPAddress.h>
#include <WS2812B.h>
#include <EEPROM.h>

#define LEDS 484
#define port_c 1338
#define port_d 1337

#define hostlen 40
#define start_addr 0

char hostname[hostlen];

// LED Strip
WS2812B strip = WS2812B(LEDS);

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

void control(uint16_t dest_port, uint8_t src_ip[4], uint16_t src_port, const char *data, uint16_t len) {
  
}

void eeprom_read(byte* array, int &address, int len) {
  // Read from address, for len bytes, modifying buffer array
  for (int i = 0; i < len; i++) {
    array[i] = EEPROM.read(address);
    ++address;
  }
}


void setup(){
  int address = start_addr;
  byte mac[6] = {0, };
  eeprom_read(mac, address, sizeof(mac));

  byte buf[4] = {0, };
  eeprom_read(buf, address, sizeof(buf));
  byte loc_ip[] = {buf[0], buf[1], buf[2], buf[3]};

  eeprom_read(buf, address, sizeof(buf));
  byte sn[] = {buf[0], buf[1], buf[2], buf[3]};

  eeprom_read(buf, address, sizeof(buf));
  byte gw[] = {buf[0], buf[1], buf[2], buf[3]};

  for (int i = 0; i < hostlen; i++) {
    byte c = EEPROM.read(address);
    ++address;
    hostname[i] = c;
    if (c == 0) {
      break;
    }
  }
  
  // Start strip
  strip.begin();
  strip.setBrightness(255);

  if (ether.begin(sizeof Ethernet::buffer, mac) == 0){}
  else{}
  ether.staticSetup(loc_ip, gw);
  ether.udpServerListenOnPort(&udpData, port_d);
  ether.udpServerListenOnPort(&control, port_c);
}

void loop(){
  ether.packetLoop(ether.packetReceive());
}
