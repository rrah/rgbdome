#include <EEPROM.h>

#define start_addr 0

// EEPROM order - mac[6], ip[4], sn[4], gw[4], host[40]

byte hostname[] = "control-01";
byte mac[] = {0x92, 0x00, 0x00, 0x00, 0x00, 0x00};
byte loc_ip[4] = {192, 168, 10, 7};
byte gw[4] = {192, 168, 10, 1};
byte sn[4] = {255, 255, 255, 0};

void eeprom_write(byte* array, int &address, int len) {
  for (int i = 0; i < len; i++) {
    EEPROM.write(address, array[i]);
    ++address;
  }
}

void eeprom_setup() {
  EEPROM.write(0, 255);
  int address = start_addr;
  eeprom_write(mac, address, 6);
  eeprom_write(loc_ip, address, 4);
  eeprom_write(sn, address, 4);
  eeprom_write(gw, address, 4);
  eeprom_write(hostname, address, sizeof(hostname));
}

void setup() {
  eeprom_setup();
}

void loop() {}
