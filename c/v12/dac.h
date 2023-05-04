
#ifndef DAC_H
#define DAC_H

#include <stdio.h>
#include "pico/stdlib.h"
#include <utility>
#include <map>
#include <string>
#include <vector>
#include <algorithm>

#include "defines.h"

using namespace std;

class dac_t {
  public:
  map<string, pair<int, int>> lut;

  dac_t() {
    this->lut["vdd"]       = pair<int, int>(0, CS_LDO);
    this->lut["avdd_cim"]  = pair<int, int>(1, CS_LDO);
    this->lut["avdd_sram"] = pair<int, int>(2, CS_LDO);

    this->lut["avdd_bl"]   = pair<int, int>(0, CS_AVDD);
    this->lut["avdd_wl"]   = pair<int, int>(1, CS_AVDD);
    this->lut["vref"]      = pair<int, int>(2, CS_AVDD);

    this->lut["vb1"]       = pair<int, int>(0, CS_BIAS);
    this->lut["vb0"]       = pair<int, int>(1, CS_BIAS);
    this->lut["vbl"]       = pair<int, int>(2, CS_BIAS);
    this->lut["vb_dac"]    = pair<int, int>(3, CS_BIAS);

    this->init();
  }
  ~dac_t() { }

  void init() {
    this->set_voltage("vdd",       790);
    this->set_voltage("vdd",       790);
    this->set_voltage("avdd_cim",  820);
    this->set_voltage("avdd_sram", 850);

    this->set_voltage("avdd_bl", 900);
    this->set_voltage("avdd_wl", 450);
    this->set_voltage("vref",    400);

    this->set_voltage("vb1",    500);
    this->set_voltage("vb0",    450);
    this->set_voltage("vbl",    250);
    this->set_voltage("vb_dac", 900);
  }

  void set_voltage(string name, uint32_t value, bool verbose) {
    if (verbose) printf("%s: %d\n", name.c_str(), value);
    this->set_voltage(name, value);
  }

  void set_voltage(string name, uint32_t value) {
    uint32_t code = value * 256 / 1200;
    this->set_dac(name, code);
  }

  void set_dac(string name, uint32_t code) {
    pair<int, int> id = this->lut[name];
    this->write(id.second, id.first, code);
  }

  /*
  void write(int sync, int address, int data) {
    // PD = 1
    // LDAC = 0
    // last = 0000
    // bits = address + PD + LDAC + data + last

    uint32_t PD = 1;
    uint32_t LDAC = 0;
    uint32_t last = 0;

    uint32_t bits = 0x0000;
    bits = bits | (last    << 0);
    bits = bits | (data    << 4);
    bits = bits | (LDAC    << 12);
    bits = bits | (PD      << 13);
    bits = bits | (address << 14);

    gpio_put(sync, 0); sleep_us(1);
    for (int i=15; i>=0; i--) {
      uint32_t bit = (bits >> i) & 0x1;
      gpio_put(MOSI, bit); sleep_us(1);
      gpio_put(SCK,  1);   sleep_us(1);
      gpio_put(SCK,  0);   sleep_us(1);
    }
    gpio_put(sync, 1); sleep_us(1);
  }
  */

  void write(int sync, int addr, int data) {
    // PD = 1
    // LDAC = 0
    // last = 0000
    // bits = address + PD + LDAC + data + last

    vector<uint8_t> _addr = int_to_bits(addr, 2);
    reverse(_addr.begin(),_addr.end());

    vector<uint8_t> _data = int_to_bits(data, 8);
    reverse(_data.begin(),_data.end());

    vector<uint8_t> PD{1};
    vector<uint8_t> LDAC{0};
    vector<uint8_t> last(4, 0);

    vector<uint8_t> bits;
    bits.insert(bits.end(), _addr.begin(), _addr.end());
    bits.insert(bits.end(), PD.begin(), PD.end());
    bits.insert(bits.end(), LDAC.begin(), LDAC.end());
    bits.insert(bits.end(), _data.begin(), _data.end());
    bits.insert(bits.end(), last.begin(), last.end());

    /*
    for (int i=0; i<16; i++) {
      printf("%d", bits[i]);
    }
    printf("\n");
    */

    gpio_put(sync, 0); sleep_us(1);
    for (int i=0; i<16; i++) {
      gpio_put(MOSI, bits[i]); sleep_us(1);
      gpio_put(SCK,  1);       sleep_us(1);
      gpio_put(SCK,  0);       sleep_us(1);
    }
    gpio_put(sync, 1); sleep_us(1);
  }
};

#endif
