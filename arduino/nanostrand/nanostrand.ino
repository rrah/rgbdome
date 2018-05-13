#include <EtherCard.h>
#include <IPAddress.h>
#include <Adafruit_NeoPixel.h>

#define LEDS 240
#define LED_PIN 6

//LED setup
Adafruit_NeoPixel strip = Adafruit_NeoPixel(LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

// Network settings
static byte myip[] = { 192,168,10,6 };
static byte gwip[] = { 192,168,10,254 };
static byte mymac[] = { 0x70,0x69,0x69,0x2D,0x30,0x31 };

byte Ethernet::buffer[(LEDS * 3) + 43]; // tcp/ip send and receive buffer

//callback that prints received packets to the serial port
void udpData(uint16_t dest_port, uint8_t src_ip[IP_LEN], uint16_t src_port, const char *data, uint16_t len){
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
  Serial.begin(57600);

  // Start strip
  strip.begin();
  strip.setBrightness(255);

  if (ether.begin(sizeof Ethernet::buffer, mymac, 10) == 0)
    Serial.println(F("Failed to access Ethernet controller"));
  else
    Serial.println(F("Starting Ethernet Controller"));
  ether.staticSetup(myip, gwip);

  ether.printIp("IP:  ", ether.myip);
  ether.printIp("GW:  ", ether.gwip);
  ether.printIp("DNS: ", ether.dnsip);

  ether.udpServerListenOnPort(&udpData, 1337);

  Serial.println(F("Starting ports"));
}

void loop(){
  ether.packetLoop(ether.packetReceive());
}
