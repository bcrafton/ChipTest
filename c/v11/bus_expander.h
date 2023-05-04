
#ifndef BUS_EXPANDER_H
#define BUS_EXPANDER_H

#include <stdio.h>
#include "pico/stdlib.h"
#include <utility>
#include <map>
#include <string>
#include <vector>
#include <algorithm>

#include "defines.h"

using namespace std;

class bus_expander_t {
  public:

  bus_expander_t() {
    this->init();
  }
  ~bus_expander_t() { }

  void init() {
    this->write(0, 0);
    this->write(9, 0xff);
  }
  
  void write(int address, int data) {
    // opcode = 01000
    // A1 = 0
    // A0 = 0
    // rw = 0
    // opcode | A1 | A0 | rw = 0x40
    
    gpio_put(CS_EN, 0); sleep_us(1);
    this->send(0x40);
    this->send(address);
    this->send(data);
    gpio_put(CS_EN, 1); sleep_us(1);
  }
  
  void send(int bits) {
    for (int i=7; i>=0; i--) {
      uint32_t bit = (bits >> i) & 0x1;
      gpio_put(MOSI, bit); sleep_us(1);
      gpio_put(SCK,  1);   sleep_us(1);
      gpio_put(SCK,  0);   sleep_us(1);
    }
  }
};

#endif
